import json
from datetime import date, timedelta

import requests
from celery import Celery
from celery.schedules import crontab

app = Celery("tasks", broker="amqp://rabbitmq")  # backend="db+sqlite:///db.sqlite3"

app.conf.beat_schedule = {
    'every-30-secs': {
        'task': 'main.parse_hh',
        'schedule': crontab(minute=0, hour=10, day_of_week='mon'),
    }
}
app.conf.timezone = 'Europe/Moscow'


@app.task
def parse_hh():
    res = requests.get("https://api.hh.ru/vacancies?text=data,данных&archived=false&per_page=100&period=7").json()
    entries = res['items']
    found_n_pages = res['pages']
    curr_page = res['page']
    while curr_page < found_n_pages:
        curr_page += 1
        entries += requests.get("https://api.hh.ru/vacancies?text=data,данных&archived=false&per_page=100"
                                "&page=" + str(curr_page) + "&period=7").json()['items']

    employers = set([entry['employer']['name'] for entry in entries])
    vac_num_by_employers = {employer: 0 for employer in employers}

    for entry in entries:
        vac_num_by_employers[entry['employer']['name']] += 1
    max_n = max(vac_num_by_employers.values())
    sorted_employers = {k: v for k, v in sorted(vac_num_by_employers.items(), key=lambda item: item[1])}
    top_employers = dict(filter(lambda el: el[1] >= max_n / 10, sorted_employers.items()))

    file = open("samples/top_employers" + str(date.today()) + ".csv", "w")
    date.today()
    for i in top_employers.items():
        file.write(i[0] + ", " + str(i[1]) + "\n")
    file.close()

    response = requests.post('https://hooks.slack.com/services/***',
                             headers={'Content-type': 'application/json'},
                             data=json.dumps(
                                 ({"text": "За эту неделю появилось " + str(res['found']) + " новых вакансий(minkovichei@gmail.com)"})))
    print(response.status_code)


if __name__ == '__main__':
    parse_hh()

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from celery import Celery
import sqlalchemy

app = Celery("tasks", backend="db+sqlite:///db.sqlite3", broker="amqp://localhost:5672")


@app.task
def reverse(text):
    return text[::-1]


def parse_hh():
    res = requests.get("https://api.hh.ru/vacancies?text=data,данных&archived=false&per_page=100&period=8").json()
    entries = res['items']
    found_n_pages = res['pages']
    curr_page = res['page']
    while curr_page + 1 < found_n_pages:
        curr_page += 1
        entries = entries + requests.get("https://api.hh.ru/vacancies?text=data,данных&archived=false&per_page=100"
                                    "&page=" + str(curr_page) + "&period=8").json()['items']
    print(len(set([entry['id'] for entry in entries])))
    print(res['found'])


if __name__ == '__main__':
    parse_hh()


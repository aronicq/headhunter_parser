[По-русски](README.md)/In english

Hh.ru service parser set up to look for data-related vacancies

To start:

docker-compose up


Both containers will start
parsing every monday hh.ru with data-related vacancies created last week,
then their number will be sent to slack channel, 
dump with employers that have number of vacancies greater than most will be placed in samples folder.

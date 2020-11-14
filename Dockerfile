FROM python:3
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

WORKDIR /
RUN pip install --no-cache-dir celery requests
COPY . /
WORKDIR /py_script
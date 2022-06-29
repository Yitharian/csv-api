FROM python:3.9

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /requirements.txt
COPY requirements/base.txt /requirements/base.txt

COPY mitigapi /opt/mitigapi

RUN pip install -r /requirements.txt

WORKDIR /opt/mitigapi

CMD python manage.py runserver 0.0.0.0:8000

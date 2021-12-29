# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /Flask

RUN pip3 install flask
RUN apt-get update
RUN apt-get install nano -y
RUN pip3 install google-cloud-storage
RUN pip3 install google-cloud-bigquery

COPY . .

CMD ["python", "./main.py", "--host=0.0.0.0"]

# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /Flask

RUN pip3 install flask

COPY . .

CMD ["python", "./main.py", "--host=0.0.0.0"]

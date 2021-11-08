# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /Flask

RUN pip3 install flask
RUN RUN apt-get update
Run apt-get install nano -y

COPY . .

CMD ["python", "./main.py", "--host=0.0.0.0"]

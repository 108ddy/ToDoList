FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN apt-get install -y netcat

RUN pip3 install --upgrade pip

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./docker-entrypoint.sh .

RUN chmod +x docker-entrypoint.sh

COPY . .

CMD ["bash", "docker-entrypoint.sh"]

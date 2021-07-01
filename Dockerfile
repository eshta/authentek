FROM python:3.8.11-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y postgresql gcc python3-dev musl-dev libffi-dev bash make automake
RUN pip install --upgrade pip

ADD ./requirements.txt /usr/src/app/requirements.txt
ADD ./requirements-dev.txt /usr/src/app/requirements-dev.txt
ADD ./.docker /usr/src/app/.docker

RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"

WORKDIR /usr/src/app/

RUN ls -la .docker/
RUN ls -la /usr/src/app/.docker/entrypoint.sh

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

RUN echo "0.0.0.0   auth.local" >> /etc/hosts

#COPY . /usr/src/app/

EXPOSE 8888


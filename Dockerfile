FROM python:3.8

COPY . /src

COPY ./requirements.txt /src/requirements.txt

WORKDIR src

EXPOSE 8000:8000

RUN pip install -r requirements.txt



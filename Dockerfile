FROM python:3.8

COPY . /src

COPY ./requirements.txt /src/requirements.txt

WORKDIR src

EXPOSE 8000:8000

ENV PATH="/scripts:/py/bin:$PATH"

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

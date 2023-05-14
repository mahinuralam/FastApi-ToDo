FROM python:3.9

WORKDIR /FastApi-ToDo

COPY ./requirements.txt /FastApi-ToDo

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /FastApi-ToDo

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

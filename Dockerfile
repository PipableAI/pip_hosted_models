
FROM python:3.10

WORKDIR /code

COPY requirements.txt .

RUN pip3.10 install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 3200

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "backend:app"]
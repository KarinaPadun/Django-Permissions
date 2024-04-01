FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY messenger_project .

CMD ["gunicorn", "messenger.wsgi:application", "--bind", "0.0.0:8000"]

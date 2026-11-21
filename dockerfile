
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV AWS_REGION=us-east-1
ENV DB_SECRET_NAME="rds!db-aaaae91b-0a32-4b2d-bafa-064409291c91"

ENV DB_HOST="database-1.clawymg4ez8q.us-east-1.rds.amazonaws.com"
ENV DB_NAME="mydb"
ENV DB_PORT=3306

ENV FRONTEND_ORIGIN="*"

EXPOSE 5000

CMD ["python", "app.py"]


FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DB_HOST="database-1.clawymg4ez8q.us-east-1.rds.amazonaws.com"
ENV DB_USER="admin"
ENV DB_PASSWORD="qwerty123"
ENV DB_NAME="mydb"
ENV DB_PORT="3306"

ENV FRONTEND_ORIGIN="*"

EXPOSE 5000

CMD ["python", "app.py"]

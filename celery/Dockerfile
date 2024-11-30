FROM python:3.9-slim

WORKDIR /app

COPY ./celery/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./celery /app

COPY ./feedback_service/tasks /app/tasks
COPY ./feedback_service/sentiment /app/sentiment

ENV PYTHONPATH=/app

CMD ["celery", "-A", "celery_task", "worker", "--loglevel=info"]

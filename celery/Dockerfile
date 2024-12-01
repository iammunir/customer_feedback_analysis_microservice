FROM python:3.9-slim

WORKDIR /app

COPY ./celery/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader punkt_tab
RUN python -m nltk.downloader vader_lexicon

COPY ./celery /app

COPY ./feedback_service/tasks /app/tasks
COPY ./feedback_service/sentiment /app/sentiment

ENV PYTHONPATH=/app

CMD ["celery", "-A", "celery_task", "worker", "--loglevel=info"]

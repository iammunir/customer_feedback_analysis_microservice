import sys
import os
from celery import Celery

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Celery('feedback_service')

app.config_from_object('config')

app.autodiscover_tasks(['tasks.tasks'])

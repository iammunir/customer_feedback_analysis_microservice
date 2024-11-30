import os
from pathlib import Path
from decouple import AutoConfig

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = os.path.join(BASE_DIR, '.env')

print('env_path:', env_path)

# Load .env variables
if os.path.exists(env_path):
    config = AutoConfig(env_path)
    broker_url = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
    result_backend = config('CELERY_RESULT_BACKEND', default='db+postgresql://postgres:admin@localhost:5432/feedback_db')
    result_extended = config('CELERY_RESULT_EXTENDED', default=True)
    result_persistent = config('CELERY_RESULT_PERSISTENT', default=True)
    task_serializer = config('CELERY_TASK_SERIALIZER', default='json')
else:
    broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    result_backend = os.getenv('CELERY_RESULT_BACKEND', 'db+postgresql://postgres:admin@localhost:5432/feedback_db')
    result_extended = os.getenv('CELERY_RESULT_EXTENDED', True)
    result_persistent = os.getenv('CELERY_RESULT_PERSISTENT', True)
    task_serializer = os.getenv('CELERY_TASK_SERIALIZER', 'json')

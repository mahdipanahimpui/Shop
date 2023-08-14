from celery import Celery
from datetime import timedelta
import os

### to use media in cdns manually use celery ###

# set an environment variable to define where is the config files
# second arg is proj_name.settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Shop.settings') # NOTE check the setting direction

celery_app = Celery('Shop') # should be project name
celery_app.autodiscover_tasks() # discover task in all apps (finds the tasks.py)


celery_app.conf.broker_url = "amqp://guest:guest@localhost:5672"
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'pickle'
celery_app.conf.accept_content = ['json', 'pickle']
celery_app.conf.result_expires = timedelta(days=1)
celery_app.conf.task_always_eager = False # by default False, not block the client
celery_app.conf.worker_prefetch_multiplier = 1 # by default is 4



# import the celery_app in __init__.py in project
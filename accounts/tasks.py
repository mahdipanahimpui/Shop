from celery import shared_task
from datetime import datetime, timedelta
from accounts.models import OtpCode
import pytz

@shared_task # after add this task run server and the celery again
def remove_expired_otp_codes():
    expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
    OtpCode.objects.filter(created__lt=expired_time).delete()





### WARNING ###
## after set the periodic tastk in admin panel: 
# run 2 terminal in env:
# first: celery -A proj worker -l INFO
# second: celery -A proj beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
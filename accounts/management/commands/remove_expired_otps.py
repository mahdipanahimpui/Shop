# by <python manage.py help> command, can see the statements,
# HOW add an command to manage.py

# create managemnet directory in app directory
# create __init__.py in management dir
# create commands directory in management directory
# create your own .py file 



from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta
import pytz # pip install pytz


# class name should be <Command> 
class Command(BaseCommand):
    help = 'remove all expired otp codes'

    # overwride the handle def
    def handle(self, *args, **kwargs):
        expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expired_time).delete()

        self.stdout.write('all expired otp code removed.')



## use <python manage.py remove_expired_otps> to run the commands



### use automatically by celery beat
# pip install django-celery-beat
# add <django_celery_beat> in installed app, makemigrations and migrate

## in django Admin panne:
# solar event: by latitude and longitude
# clocked: for a specific time
# interval: in every 20 days, one time 
# crontab: like linux >> *****
# * means every of these
# minute(0-59) hour(0-23) day(0-31) month(0=none and 12=december) day_of_week(0=sunday and 7=sunday)


# periodic task: which task should run periodically







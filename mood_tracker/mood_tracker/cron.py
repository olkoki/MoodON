from django_cron import CronJobBase, Schedule
from .models import DailyRoutine
from datetime import date, timedelta

class DeleteRoutineCronJob(CronJobBase):
    RUN_EVERY_MIDNIGHT = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MIDNIGHT)
    code = 'mood_tracker.delete_routine_cron_job'

    def do(self):
        today = date.today()
        yesterday = today - timedelta(days=1)
        DailyRoutine.objects.filter(date=yesterday).delete()

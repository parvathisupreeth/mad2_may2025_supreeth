from flask_caching import Cache
from celery import Celery
from celery.schedules import crontab

cache = Cache()


def make_celery(app_name=__name__):
    _celery = Celery(
        app_name,
        backend="redis://localhost:6379/0",
        broker="redis://localhost:6379/0",
        include=["tasks"]          # <-- always load tasks.py on worker start
    )
    _celery.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="Asia/Kolkata",
        enable_utc=False,
        beat_schedule={
            # Job a: daily deadline reminders at 8:00 AM IST
            "send-daily-deadline-reminders": {
                "task": "tasks.send_daily_deadline_reminders",
                "schedule": crontab(hour=8, minute=0),
            },
            # Job b: monthly report on 1st of every month at 7:00 AM IST
            "send-monthly-activity-report": {
                "task": "tasks.send_monthly_report",
                "schedule": crontab(hour=7, minute=0, day_of_month=1),
            },
        },
    )
    return _celery


celery = make_celery()

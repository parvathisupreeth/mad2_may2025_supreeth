from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "placement_portal",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=False,


    beat_schedule={

  
        "send-daily-deadline-reminders": {
            "task": "tasks.send_daily_deadline_reminders",
            "schedule": crontab(hour=8, minute=0),
        },


        "send-monthly-activity-report": {
            "task": "tasks.send_monthly_report",
            "schedule": crontab(hour=7, minute=0, day_of_month=1),
        },
    },
)
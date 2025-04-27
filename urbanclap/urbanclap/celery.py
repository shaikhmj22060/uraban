
import os
from celery import Celery
import service_provider.tasks
import dashboard.tasks
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "urbanclap.settings")

app = Celery("urbanclap")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
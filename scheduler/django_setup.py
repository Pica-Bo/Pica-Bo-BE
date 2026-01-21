import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "scheduler.settings",  # <-- adjust to your Django project
)

django.setup()

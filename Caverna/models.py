from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.query_utils import Q
from model_utils import FieldTracker


class User(AbstractUser):
    pass
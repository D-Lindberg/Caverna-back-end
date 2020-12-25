from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.query_utils import Q
from model_utils import FieldTracker

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=False)

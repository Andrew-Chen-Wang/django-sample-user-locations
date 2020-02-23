from django.contrib.gis.db import models  # This also imports standard models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    location = models.PointField()  # Default spatial_index: True

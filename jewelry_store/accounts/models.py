from django.db import models
from django.contrib.auth.models import User  # Thêm dòng này

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)

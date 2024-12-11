from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class User_Room(models.Model):
    room_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=False)
    room_host = models.ForeignKey(User, on_delete=models.CASCADE)
    room_password = models.TextField()
    
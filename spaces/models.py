from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Space(models.Model):
    space_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15)
    keyword = models.CharField(max_length=15, blank=True)
    max_capacity = models.IntegerField(validators=[MaxValueValidator(12)])
    duration_days = models.IntegerField(validators=[MinValueValidator(30), MaxValueValidator(365)])
    is_public = models.BooleanField(default=True)
    record_cycle = models.CharField(max_length=50)
    record_limit = models.CharField(max_length=50)
    invite_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.space_id}] {self.name}"
    
class SpaceMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='members')
    joined_at = models.DateTimeField(auto_now_add=True)
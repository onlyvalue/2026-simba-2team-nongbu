from django.db import models
from spaces.models import Space
from django.contrib.auth.models import User

class star(models.Model):
    star = models.BigAutoField(primary_key=True)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}님의 별"
from django.db import models
# Create your models here.

class Friend(models.Model):
    user=models.CharField(max_length=120)
    friend=models.CharField(max_length=120)
    nickname=models.CharField(max_length=120)

    def __str__(self):
        return f"Friend of {self.user} is {self.friend}"
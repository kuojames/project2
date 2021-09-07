from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.PositiveIntegerField(default=160)
    male = models.BooleanField(default=False)
    website = models.URLField(null=True)

    def __str__(self):
        return self.user.username

class Poll(models.Model):
    name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Poll_item(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    img = models.ImageField(upload_to='static/images/', null=False)
    vote_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name





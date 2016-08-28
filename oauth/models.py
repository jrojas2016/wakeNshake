from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class customUser(models.Model):
	user = models.OneToOneField(User,null=True, related_name='profile')
	spotify_cred = models.CharField(default= '', unique=True)
	calendar_cred = models.CharField(default= '', unique=True)



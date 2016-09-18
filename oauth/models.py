from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.
class customUser(models.Model):
	# Assuming only one user for now. Implement Front-end login before scaling
	id = models.AutoField(primary_key=True)
	# user = models.OneToOneField(User,null=True, related_name='profile')
	user_name = models.CharField(max_length=50, default='', unique=True)
	spotify_cred = models.CharField(max_length=1000,default= '', unique=True)
	calendar_cred = models.CharField(max_length=1000, default= '', unique=True)

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']



from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


# Create your models here.
class customUser(models.Model):
	user = models.OneToOneField(User,null=True, related_name='profile')
	spotify_cred = models.CharField(max_length=500,default= '', unique=True)
	calendar_cred = models.CharField(max_length=500, default= '', unique=True)



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')



from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models


# Create your models here.
class App(models.Model):

    app_name = models.CharField(max_length=30)
    app_description = models.TextField()
    app_link = models.TextField()
    default_visibility=models.BooleanField(default=True)
    created_on=models.DateTimeField(default=timezone.now())

class Subscriber(models.Model):
    
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,db_column='user_id')
    app_id = models.ForeignKey(App,on_delete=models.CASCADE,db_column='app_id')
    is_active = models.BooleanField(default=False)

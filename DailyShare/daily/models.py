import datetime

from django.db import models


# Create your models here.


# 表模型




class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    token = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)

class Plan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,default='')
    plan_name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    # start = models.TimeField(default=datetime.datetime.now())
    # end = models.TimeField(default=datetime.datetime.now())#yiyibaobao
    state = models.BooleanField(default=False)
    is_fixed = models.BooleanField()

class Record(models.Model):
    record_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,default='')
    plan_name =models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField(default=datetime.datetime.now)
    upload = models.BooleanField(default=False)

    @property
    def duration(self):
        return self.end - self.start





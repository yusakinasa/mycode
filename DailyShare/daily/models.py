import datetime

from django.db import models

# Create your models here.


# 表模型

class Welcome(models.Model):
    img = models.ImageField(upload_to='welcome',default='/welcome/slash.jpg')
    order = models.IntegerField()
    create_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)



class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    usr_name = models.CharField(max_length=100)
class Plan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start = models.TimeField(default=datetime.datetime.now())
    end = models.TimeField(default=datetime.datetime.now())#yiyibaobao
    state = models.BooleanField(default=False)
    is_fixed = models.BooleanField()




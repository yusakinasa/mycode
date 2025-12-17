from django.urls import path
from django.contrib import admin

from daily.views import *

urlpatterns = [
    path('fplan/',fixed_plan),
    path('plan/<int:plan_id>',plan_detail),
    path('records/',record),
    path('record/<int:record_id>',record_detail),
]
from django.contrib import admin

# Register your models here.


from .models import*

admin.site.register(Welcome)
admin.site.register(User)
admin.site.register(Plan)
admin.site.register(Record)
from django.contrib import admin
from calender.models import *
# Register your models here.

class CustomuserAdmin(admin.ModelAdmin):
    list_display = ['id', 'state', 'resolved']

admin.site.register(CustomUser, CustomuserAdmin)
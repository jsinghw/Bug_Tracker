from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import MyUser, Tickets


# Register your models here.
admin.site.register(MyUser, UserAdmin)
admin.site.register(Tickets)

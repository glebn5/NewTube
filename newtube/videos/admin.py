from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User, UserAdmin) #добавление в адмику таблицы Useer
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Tags)
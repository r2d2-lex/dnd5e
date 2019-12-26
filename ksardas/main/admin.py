from django.contrib import admin

# Register your models here.
from .models import AdvUser, CharBase

admin.site.register(AdvUser)
admin.site.register(CharBase)

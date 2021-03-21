from django.contrib import admin

from .models import Profile,department




admin.site.register(Profile)
# Register your models here.

#new
admin.site.register(department)

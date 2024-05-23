from django.contrib import admin
from .models import Component,Type,Manufacturer,UserSession

admin.site.register(Component)
admin.site.register(Type)
admin.site.register(Manufacturer)
admin.site.register(UserSession)

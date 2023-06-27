from django.contrib import admin

# Register your models here.

from .models import Staff, Asset, Categories, Department, Event, Predict

admin.site.register(Department)
admin.site.register(Staff)
admin.site.register(Categories)
admin.site.register(Asset)
admin.site.register(Event)
admin.site.register(Predict)

from django.contrib import admin

# Register your models here.

from .models import Staff, Asset, Order, Categories

admin.site.register(Staff)
admin.site.register(Categories)
admin.site.register(Asset)
admin.site.register(Order)

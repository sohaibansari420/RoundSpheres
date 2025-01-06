from django.contrib import admin

# Register your models here.
from home.models import User, Order, Product

admin.site.register(User)
"""admin.site.register(Iotdata)"""
"""admin.site.register(Analytic)"""
admin.site.register(Product)
admin.site.register(Order)
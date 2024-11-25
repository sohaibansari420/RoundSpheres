from django.contrib import admin

# Register your models here.
from .models import User, Iotdata, Analytic, Product

admin.site.register(User)
admin.site.register(Iotdata)
admin.site.register(Analytic)
admin.site.register(Product)
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
 
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("shop", views.shop, name='shop'),
    path("blog", views.blog, name='blog'),
    path("login", views.login, name='login'),
    path("data", views.data, name='data'),

]
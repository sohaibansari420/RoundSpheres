from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
 
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("shop", views.shop, name='shop'),
    path("blog", views.blog, name='blog'),
    path("login/", views.login, name='login'),
    path("signup/", views.signup, name='signup'),
    path("data", views.data, name='data'),
    # # Detail views for Apidata
    # path('apidata/<int:dataId>/', views.ApidataDetailView.as_view(), name='apidata-detail'),
    # # Detail views for Users
    # path('user/<int:profileId>/', views.UserDetailView.as_view(), name='user-detail'),\
    # # Detail views for Product
    # path('product/<int:productId>/', views.ProductDetailView.as_view(), name='product-detail'),
    # # Detail views for Analytic
    # path('analytic/<int:analyticId>/', views.AnalyticDetailView.as_view(), name='analytic-detail')
]
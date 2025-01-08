from django.contrib import admin
from django.urls import path,include
from home import views
from . import views
# from django.contrib.auth import views as auth_views

urlpatterns = [
 
    path("", views.index, name='home'),
    path("about/", views.about, name='about'),
    path("contact/", views.contact, name='contact'),
    path("shop/", views.shop, name='shop'),
    path("blog/", views.blog, name='blog'),
    path("auth/signup/", views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path("auth/", include("django.contrib.auth.urls")),
    # path('auth/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path("data/", views.data, name='data'),
    # path("logout", views.logout, name='logout'),
    
    # # Detail views for Apidata
    # path('apidata/<int:dataId>/', views.ApidataDetailView.as_view(), name='apidata-detail'),
    # # Detail views for Users
    # path('user/<int:profileId>/', views.UserDetailView.as_view(), name='user-detail'),\
    # # Detail views for Product
    # path('product/<int:productId>/', views.ProductDetailView.as_view(), name='product-detail'),
    # # Detail views for Analytic
    # path('analytic/<int:analyticId>/', views.AnalyticDetailView.as_view(), name='analytic-detail')
    # path('products/', views.products_view, name='products'),
    # path('signup/', views.signup, name='register'),
    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),

#    Url to send emails
    path("sendemails", views.sendemails, name='sendemails'),
    path("shopview", views.shopview, name='shopview'),
]


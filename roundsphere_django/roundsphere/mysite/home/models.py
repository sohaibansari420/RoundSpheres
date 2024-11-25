from django.db import models
from django.urls import reverse

import uuid # Required for unique IDs

# Create your models here.
#--------------------------------------------------------------------------------------------------------------------
# User Model
class User(models.Model):
    """Definition of the User Model in Django"""
    profileId = models.AutoField(primary_key=True)
    # models.UUIDField(primary_key=True, default=uuid.uuid4)  # Auto-incrementing primary key
    firstname = models.CharField(max_length=80, null=False)  # First name, max length 80
    lastname = models.CharField(max_length=80, null=False)   # Last name, max length 80
    email = models.EmailField(max_length=80, unique=True, null=False)  # Unique email field
    role = models.CharField(max_length=80, null=False)       # Role field
    created_at = models.DateTimeField(auto_now_add=True)     # Automatically set on creation

    def __str__(self):
        return f"User {self.profileId}: {self.firstname} {self.lastname}"
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this user."""
        return reverse('user-detail', args=[str(self.profileId)])
    
    class Meta:
        db_table = 'User_data'  # Explicitly sets the table name
        ordering = ['firstname', 'lastname']  # Default ordering by first and last name
        verbose_name = 'User'
        verbose_name_plural = 'Users'

#--------------------------------------------------------------------------------------------------------------------
# IoT Data Model
class Iotdata(models.Model):
    """Definition of the Iotdata Model in Django"""
    dataId = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    temperatureWater = models.CharField(max_length=80, null=False)  # Water temperature as a string
    temperatureAir = models.CharField(max_length=80, null=False)   # Air temperature as a string
    humidity = models.CharField(max_length=80, null=False)         # Humidity as a string
    windSpeed = models.CharField(max_length=80, null=False)        # Wind speed as a string
    precipitation = models.CharField(max_length=80, null=False)    # Precipitation as a string
    notes = models.TextField(null=False)                           # Notes with up to 200 characters
    created_at = models.DateTimeField(auto_now_add=True)           # Automatically set on creation

    def __str__(self):
        return f"Iotdata {self.dataId}"
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this Apidata."""
        return reverse('iotdata-detail', args=[str(self.dataId)])
    
    class Meta:
        db_table = 'IoT_data'  # Explicitly sets the table name
        ordering = ['-created_at']  # Orders by most recent data first
        verbose_name = 'IoT Data'
        verbose_name_plural = 'IoT Data Records'

#--------------------------------------------------------------------------------------------------------------------
# Analytic Data Model
class Analytic(models.Model):
    """Definition of the Analytic Model in Django"""
    analyticId = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    region = models.CharField(max_length=80, null=False)  # Region field
    evaporationRate = models.FloatField(null=True)  # Evaporation rate as a float
    trend = models.CharField(max_length=80, null=False)  # Trend field
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for record creation

    def __str__(self):
        return f"Analytic {self.analyticId}: {self.region}"

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this Analytic."""
        return reverse('analytic-detail', args=[str(self.analyticId)])
    
    class Meta:
        db_table = 'Analytic_data'  # Explicitly sets the table name
        ordering = ['region', '-created_at']  # Orders by region, then most recent data
        verbose_name = 'Analytic Data'
        verbose_name_plural = 'Analytic Data Records'

#--------------------------------------------------------------------------------------------------------------------
# Product Model
class Product(models.Model):
    """Definition of the Product Model in Django"""
    productId = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    name = models.CharField(max_length=80, null=False)  # Product name, max length 80
    description = models.TextField(null=False)  # Product description, allows longer text
    price = models.FloatField(null=True)  # Product price as a floating-point value
    stock = models.IntegerField(null=True)  # Stock quantity as an integer
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the product is created

    def __str__(self):
        return f"Product {self.productId}: {self.name}"
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this product."""
        return reverse('product-detail', args=[str(self.productId)])
    
    class Meta:
        db_table = 'Product_data'  # Explicitly sets the table name
        ordering = ['name']  # Orders alphabetically by product name
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
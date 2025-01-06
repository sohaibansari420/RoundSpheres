from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

import uuid # Required for unique IDs

""" Create your models here."""
"""--------------------------------------------------------------------------------------------------------------"""
""" User Model """
class User(AbstractUser):
    ROLES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('researcher', 'Researcher'),
    ]
      
    """Definition of the User Model in Django"""
    userId = models.AutoField(primary_key=True)
    # models.UUIDField(primary_key=True, default=uuid.uuid4)  # Auto-incrementing primary key
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLES, default='researcher')
    email_verified = models.BooleanField(default=False)  # New field to track email verification
    firstname = models.CharField(max_length=80, null=False)  # Optional, since AbstractUser has first_name
    lastname = models.CharField(max_length=80, null=False)   # Optional, since AbstractUser has last_name
    def __str__(self):
        return f"User {self.userId}: {self.firstname} {self.lastname} - {self.role}"
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this user."""
        return reverse('user-detail', args=[str(self.userId)])
    
    class Meta:
        db_table = 'User_data'  # Explicitly sets the table name
        ordering = ['firstname', 'lastname']  # Default ordering by first and last name
        verbose_name = 'User'
        verbose_name_plural = 'Users'

"""--------------------------------------------------------------------------------------------------------------"""
""" Product Model """
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
        
"""--------------------------------------------------------------------------------------------------------------"""
""" Order Model """
class Order(models.Model):
    STATUS_CHOICES = [
     ('Pending', 'Pending'),
     ('Shipped', 'Shipped'),
     ('Completed', 'Completed'),
     ('Cancelled', 'Cancelled'),
    ]
    
    """Definition of the Order Model in Django"""
    orderId = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    userId = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to Django's User model
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to Product model
    quatity = models.PositiveIntegerField(null=True)  # Stock quantity as an integer
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2)  # Product price as a floating-point value
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the product is created

    def save(self, *args, **kwargs):
        # Automatically calculate the total_price based on quantity and product price
        if not self.totalPrice:
            self.totalPrice = self.productId.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.orderId}: {self.userId.username}"
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this order."""
        return reverse('order-detail', args=[str(self.orderId)])
    
    class Meta:
        db_table = 'Order_data'  # Explicitly sets the table name
        ordering = ['orderId']  # Orders alphabetically by Order Id
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        
        
  
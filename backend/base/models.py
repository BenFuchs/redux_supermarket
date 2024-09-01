from django.db import models
from django.contrib.auth.models import User
import datetime

# Profile model to extend the User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links each Profile to one User
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

# Product model
class Product(models.Model):
    desc = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.desc
    

# Cart model
class Cart(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to User (not Profile, to maintain backward compatibility)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    date = models.DateField(("Date"), default=datetime.date.today)

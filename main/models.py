from operator import mod
from unittest import defaultTestLoader
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey, OneToOneField
from multiselectfield import MultiSelectField

CATEGORIES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('B', 'Baby'),
        ('T', 'Traditional'),
        ('O', 'Modern'),
        ('C', 'Classic'),
    ]

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone_no1 = models.TextField(max_length=10, null=True)
    phone_no2 = models.TextField(max_length=10, null=True)
    gen_size = models.IntegerField(null=True)
    #group = Group.objects.get(name='Customers')
    #group.user_set.add(user)

def tailor_profile_path(instance, filename):
    return f'Tailor_{instance.user.id}/profile_image/images/{filename}'
def tailor_background_path(instance, filename):
    return f'Tailor_{instance.user.id}/background_image/images/{filename}'
class Tailor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone_no = models.IntegerField(null=True)

    gender_spec = MultiSelectField(max_length=6, choices=CATEGORIES, default='M',
                                   max_choices=6)

    location = models.TextField(null=True)
    
    RATING = [
        (1, 'Bad'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    ]
    rating = models.IntegerField(choices=RATING, default=3)
    profile_image = models.ImageField(upload_to = tailor_profile_path, default='Tailor_12/profile_image/images/blank-profile-picture-gc048af202_1280.png')
    background_image = models.ImageField(upload_to = tailor_background_path, default='Tailor_12/background_image/images/paper-g0b57e8602_1920.jpg')

def cloth_image_path(instance, filename):
    return f'Tailor_{instance.company_name.id}/images/{filename}'
class Clothe(models.Model):
    company_name = models.ForeignKey(User, on_delete=CASCADE, null=False)
    category = MultiSelectField(max_length=3, choices=CATEGORIES, default='M',
                                       max_choices=2)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    image = models.ImageField(upload_to = cloth_image_path)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=False)
    address = models.TextField(null=False)
    city = models.TextField(null=False)
    state = models.TextField(null=False)
    zipcode = models.TextField(null=True)
    default = models.BooleanField(default=False)
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
RATING = [
        (1, 'Bad'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    ]

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone_no1 = models.CharField(max_length=15, null=True)
    phone_no2 = models.CharField(max_length=15, null=True)
    gen_size = models.IntegerField(null=True)
    #group = Group.objects.get(name='Customers')
    #group.user_set.add(user)

def tailor_profile_path(instance, filename):
    return f'Tailor_{instance.user.id}/profile_image/images/{filename}'
def tailor_background_path(instance, filename):
    return f'Tailor_{instance.user.id}/background_image/images/{filename}'
class Tailor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    first_name = models.CharField(null=True, max_length=225)
    last_name = models.CharField(null=True, max_length=225)
    phone_no1 = models.CharField(null=True, max_length=15)
    phone_no2 = models.CharField(null=True, max_length=15)

    gender_spec = MultiSelectField(max_length=6, choices=CATEGORIES, default='M',
                                   max_choices=6)
    rating = models.IntegerField(choices=RATING, default=3)
    profile_image = models.ImageField(upload_to = tailor_profile_path, default='Tailor_12/profile_image/images/blank-profile-picture-gc048af202_1280.png')
    background_image = models.ImageField(upload_to = tailor_background_path, default='Tailor_12/background_image/images/paper-g0b57e8602_1920.jpg')

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    first_name = models.CharField(null=True, max_length=225)
    last_name = models.CharField(null=True, max_length=225)
    phone_no1 = models.CharField(null=True, max_length=15)
    phone_no2 = models.CharField(null=True, max_length=15)

    spec = MultiSelectField(max_length=6, choices=CATEGORIES, default='M',
                                   max_choices=6)
    
    rating = models.IntegerField(choices=RATING, default=3)

def cloth_image_path(instance, filename):
    return f'Tailor_{instance.company_name.id}/images/{filename}'
class Clothe(models.Model):
    company_name = models.ForeignKey(User, on_delete=CASCADE, null=False)
    category = MultiSelectField(max_length=3, choices=CATEGORIES, default='M',
                                       max_choices=2)
    price_range = models.CharField(max_length=20)
    image = models.ImageField(upload_to = cloth_image_path)
    rating = models.IntegerField(choices=RATING, default=3)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=False)
    address = models.CharField(null=False, max_length=225)
    city = models.CharField(null=False, max_length=225)
    state = models.CharField(null=False, max_length=225)
    zipcode = models.CharField(null=True, max_length=225)
    default = models.BooleanField(default=False)

class PendingTailorReg(models.Model):
    first_name = models.CharField(null=False, max_length=225)
    last_name = models.CharField(null=False, max_length=225)
    business_name = models.CharField(null=False, max_length=225)
    ig_link = models.CharField(null=True, max_length=225)
    what_i_do = models.TextField(null=False)
    email = models.EmailField(null=False)
    address = models.CharField(null=False, max_length=225)
    city = models.CharField(null=False, max_length=225)
    state = models.CharField(null=False, max_length=225)
    zipcode = models.CharField(null=True, max_length=225)

class PendingSellerReg(models.Model):
    first_name = models.CharField(null=False, max_length=225)
    last_name = models.CharField(null=False, max_length=225)
    business_name = models.CharField(null=False, max_length=225)
    ig_link = models.CharField(null=True, max_length=225)
    what_i_do = models.TextField(null=False)
    email = models.EmailField(null=False)
    address = models.CharField(null=False, max_length=225)
    city = models.CharField(null=False, max_length=225)
    state = models.CharField(null=False, max_length=225)
    zipcode = models.CharField(null=True, max_length=225)

def fabrics_image_path(instance, filename):
    return f'Fabric_{instance.seller.id}/fabric_images/images/{filename}'
class Fabric(models.Model):
    seller = models.ForeignKey(Seller, on_delete=CASCADE, null=False)        
    type = models.CharField(null=False, default='Not specified', max_length=225)
    price = models.CharField(max_length=225)
    image = models.ImageField(upload_to = fabrics_image_path)
    
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from multiselectfield import MultiSelectField

BANK = [
    ('acc', 'Access Bank'),
    ('uba', 'UBA Bank'),
    ('zen', 'Zenith Bank') 
]
CATEGORIES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('B', 'Baby'),
        ('T', 'Traditional'),
        ('O', 'Modern'),
        ('C', 'Classic'),
    ] 
ENTITY = [
    ('S', 'Sole Proprietorship'),
    ('P', 'Partnership'),
    ('C', 'Corporation')
] 
USERS = [
    ('C', 'Custom Made'),
    ('F', 'Fabrics'),
    ('T', 'Tailors')
]
RATING = [
        (1, 'Bad'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
]
STATE = [
    ('abi', 'Abia'),
    ('lag', 'Lagos'),
    ('ogu', 'Ogun'),
    ('kog', 'Kogi')
]

FABRICS = [
        ('K', 'Ankara'),    
        ('A', 'Adire'),
        ('O', 'Aso Oke'),
        ('T', 'Atiku'),
        ('B', 'Brocades'),
        ('C', 'Chiffon'),
        ('L', 'Lace'),
        ('S', 'Silk'),
        ('T', 'Tulle'),
        ('V', 'Velvet'),
    ]
GENDER = [
    ('M', 'Male'),
    ('F', 'Female')
]

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    gender = models.CharField(max_length=1, default='M', choices=GENDER)
    phone_no1 = models.CharField(max_length=15, null=True)
    phone_no2 = models.CharField(max_length=15, null=True)
    gen_size = models.IntegerField(null=True)

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
    price = models.IntegerField(default=1000)
    image = models.ImageField(upload_to = cloth_image_path)
    rating = models.IntegerField(choices=RATING, default=3)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=False)
    address = models.CharField(null=False, max_length=225)
    city = models.CharField(null=False, max_length=225)
    state = models.CharField(null=False, max_length=225)
    zipcode = models.CharField(null=True, max_length=225)
    default = models.BooleanField(default=False)

def id_image_path(instance, filename):
    return f'''ID_{instance.business_name}/business_id/images/{filename}'''
def Partner():
    user = models.OneToOneField(User, on_delete=CASCADE, null=False)
    business_entity = models.CharField(ENTITY, 1, 'S', **('choices', 'max_length', 'default'))
    business_name = models.CharField(False, 225, **('null', 'max_length'))
    email = models.EmailField(False, **('null',))
    address = models.CharField(False, 225, **('null', 'max_length'))
    city = models.CharField(False, 225, **('null', 'max_length'))
    state = models.CharField(STATE, 3, 'lag', **('choices', 'max_length', 'default'))
    zipcode = models.CharField(True, 225, **('null', 'max_length'))
    brand_name = models.CharField(False, 255, **('null', 'max_length'))
    legal_rep_first_name = models.CharField(False, 225, **('null', 'max_length'))
    legal_rep_other_name = models.CharField(True, 225, None, **('null', 'max_length', 'default'))
    legal_rep_last_name = models.CharField(False, 225, **('null', 'max_length'))
    valid_id_card = models.ImageField(id_image_path, **('upload_to',))
    tin = models.CharField(25, **('max_length',))
    vat = models.CharField(25, **('max_length',))
    brand_type = models.CharField(USERS, 'T', 1, **('choices', 'default', 'max_length'))
    bank = models.CharField(BANK, 'acc', 3, **('choices', 'default', 'max_length'))
    account_number = models.CharField(25, **('max_length',))
    account_name = models.CharField(255, **('max_length',))

def id_pending_image_path(instance, filename):
    return f'''ID_pending_{instance.business_name}/business_id/images/{filename}'''
def PendingReg():
    '''PendingReg'''
    business_entity = models.CharField(ENTITY, 1, 'S', **('choices', 'max_length', 'default'))
    business_name = models.CharField(False, 225, **('null', 'max_length'))
    email = models.EmailField(False, **('null',))
    address = models.CharField(False, 225, **('null', 'max_length'))
    city = models.CharField(False, 225, **('null', 'max_length'))
    state = models.CharField(STATE, 3, 'lag', **('choices', 'max_length', 'default'))
    zipcode = models.CharField(True, 225, **('null', 'max_length'))
    brand_name = models.CharField(False, 255, **('null', 'max_length'))
    legal_rep_first_name = models.CharField(False, 225, **('null', 'max_length'))
    legal_rep_other_name = models.CharField(True, 225, None, **('null', 'max_length', 'default'))
    legal_rep_last_name = models.CharField(False, 225, **('null', 'max_length'))
    valid_id_card = models.ImageField(id_pending_image_path, **('upload_to',))
    tin = models.CharField(25, **('max_length',))
    vat = models.CharField(25, **('max_length',))
    brand_type = models.CharField(USERS, 'T', 1, **('choices', 'default', 'max_length'))
    bank = models.CharField(BANK, 'acc', 3, **('choices', 'default', 'max_length'))
    account_number = models.CharField(25, **('max_length',))
    account_name = models.CharField(255, **('max_length',))

def fabrics_image_path(instance, filename):
    return f'Fabric_{instance.seller.id}/fabric_images/images/{filename}'
class Fabric(models.Model):
    seller = models.ForeignKey(Seller, on_delete=CASCADE, null=False)        
    type = models.CharField(choices=FABRICS, default='K', max_length=1)
    price = models.IntegerField()
    image = models.ImageField(upload_to = fabrics_image_path)

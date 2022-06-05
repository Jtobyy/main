from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from multiselectfield import MultiSelectField

from datetime import datetime

BANK = [
    ('acc', 'Access Bank'),
    ('uba', 'UBA Bank'),
    ('zen', 'Zenith Bank'),
]

CATEGORIES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('B', 'Baby'),
    ('T', 'Traditional'),
    ('O', 'Modern'),
    ('C', 'Classic'),
]

CUSTOMCLOTHES = [
    ('CP', 'Caps'),
    ('BL', 'Blouse'),
    ('WK', 'Work pants'),
    ('JS', 'Jumpsuit'),
    ('CT', 'Crop tops'),
    ('JK', 'Jackets'),
    ('CO', 'Coats'),
    ('DR', 'Dresses'),
    ('OS', 'Off Shoulder'),
    ('BM', 'Bridesmaid'),
    ('PY', 'Pyjamas'),
    ('RB', 'Robes'),
    ('HO', 'Hoodies'),
    ('SS', 'Sweatshirt'),
    ('SW', 'Sweaters'),
    ('CA', 'Capris'),
    ('PA', 'Pants'),
    ('SW', 'Swimwear'),
    ('TP', 'Tops'),
    ('MT', 'Male Trousers'),
    ('FT', 'Female Trousers'),
    ('OT', 'Office Trousers'),
    ('SH', 'Shorts'),
    ('NK', 'Nickers'),
    ('SU', 'Suits'),
    ('CS', 'Corporate shirts'),
    ('TS', 'T-shirts'),
    ('GO', 'Gowns'),
    ('MS', 'Male Shirts'),
    ('FS', 'Female Shirts'),
    ('JE', 'Jeans'),
    ('SK', 'Skirts'),
    ('NW', 'Native Wares'),
]

STATUS = [
    ('P', 'Pending'),
    ('C', 'Confirmed'),
    ('R', 'Ready'),
    ('D', 'Delivered')
]

ENTITY = [
    ('S', 'Sole Proprietorship'),
    ('P', 'Partnership'),
    ('C', 'Corporation'),
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

USERS = [
    ('A', 'Customers'),
    ('C', 'Custom Made'),
    ('F', 'Fabric Sellers'),
    ('T', 'Tailors'),
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
    ('kog', 'Kogi'),
]

GENDER = [
    ('M', 'Male'),
    ('F', 'Female')
]

def id_customer_profile_image_path(instance, filename):
    return f'ID_{instance.user}/profile/images/{filename}'
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    profile_image = models.ImageField(upload_to = id_customer_profile_image_path, default=None, null=True)
    gender = models.CharField(max_length=1, default='M', choices=GENDER)
    phone_no1 = models.CharField(max_length=15, null=True)
    phone_no2 = models.CharField(max_length=15, null=True)
    gen_size = models.IntegerField(null=True)

class FemaleCustomerMeasurement(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=False)    
    round_neck = models.DecimalField(max_digits=5, decimal_places=2, default=13.5, null=True)
    shoulder_length = models.DecimalField(max_digits=5, decimal_places=2, default=16.1, null=True)
    back_shoulder_width = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    front_shoulder_width = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    back_width = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_waist = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    front_waist_length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    back_waist_length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    blouse_or_shirt_length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    bust_length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    under_bust_length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    bust_point_separation = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    under_bust_separation = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    high_bust = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_bust = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_under_bust = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_abdomen = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_seat_or_hips = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_thigh = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_knee = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_ankle = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    waist_to_hips = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    waist_to_knee = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    waist_to_ankle = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    outside_leg_length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    inside_leg_length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    shoulder_to_elbow = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    shoulder_to_wrist = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_bicep = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_arm = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_wrist = models.DecimalField(max_digits=5, decimal_places=2, null=True)

class MaleCustomerMeasurement(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=False)    
    round_neck = models.DecimalField(max_digits=5, decimal_places=2, default=19.5, null=True)
    shoulder_length = models.DecimalField(max_digits=5, decimal_places=2, default=14.4, null=True)
    back_shoulder_width = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    front_shoulder_width = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    back_width = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_waist = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    waist_length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    back_waist_length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    tunic_or_shirt_length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    chest_depth = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    chest_width = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_chest = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_waist = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_seat_or_hips = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_thigh = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_knee = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_ankle = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    waist_to_knee = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    waist_to_ankle = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    outside_leg_length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    inside_leg_length = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    shoulder_to_elbow = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    shoulder_to_wrist = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_bicep = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_arm = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    round_wrist = models.DecimalField(max_digits=5, decimal_places=2, null=True)

def id_image_path(instance, filename):
    return f'ID_{instance.business_name}/business_id/images/{filename}'
def id_profile_image_path(instance, filename):
    return f'ID_{instance.business_name}/business_id/profile/images/{filename}'
class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)    
    # Business Information    
    business_entity = models.CharField(choices=ENTITY, max_length=1, default='S')
    business_name = models.CharField(null=False, max_length=225)
    email = models.EmailField(null=False)
    address = models.CharField(null=False, max_length=225)
    city = models.CharField(null=False, max_length=225)
    state = models.CharField(choices=STATE, max_length=3, default="lag")
    zipcode = models.CharField(null=True, max_length=225)

    # Seller/Tailor Profile
    brand_name = models.CharField(null=False, max_length=255)
    legal_rep_first_name = models.CharField(null=False, max_length=225)
    legal_rep_other_name = models.CharField(null=True, max_length=225, default=None)
    legal_rep_last_name = models.CharField(null=False, max_length=225)
    profile_image = models.ImageField(upload_to = id_profile_image_path)
    valid_id_card = models.ImageField(upload_to = id_image_path)
    tin = models.CharField(max_length=25)
    vat = models.CharField(max_length=25)
    
    # Specialization
    brand_type = models.CharField(choices=USERS, default='T', max_length=1)
    # ig_link = models.CharField(null=True, max_length=225)

    # Bank Details
    bank = models.CharField(choices=BANK, default='acc', max_length=3)
    account_number = models.CharField(max_length=25)
    account_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.brand_name

def id_pending_image_path(instance, filename):
    return f'ID_pending_{instance.business_name}/business_id/images/{filename}'
def id_pending_profile_image_path(instance, filename):
    return f'ID_pending_{instance.business_name}/business_id/profile/images/{filename}'
class PendingReg(models.Model):
    # Business Information    
    business_entity = models.CharField(choices=ENTITY, max_length=1, default='S')
    business_name = models.CharField(null=False, max_length=225)
    email = models.EmailField(null=False)
    address = models.CharField(null=False, max_length=225)
    city = models.CharField(null=False, max_length=225)
    state = models.CharField(choices=STATE, max_length=3, default="lag")
    zipcode = models.CharField(null=True, max_length=225)

    # Seller/Tailor Profile
    brand_name = models.CharField(null=False, max_length=255)
    legal_rep_first_name = models.CharField(null=False, max_length=225)
    legal_rep_other_name = models.CharField(null=True, max_length=225, default=None)
    legal_rep_last_name = models.CharField(null=False, max_length=225)
    profile_image = models.ImageField(upload_to = id_pending_profile_image_path)
    valid_id_card = models.ImageField(upload_to = id_pending_image_path)
    tin = models.CharField(max_length=25)
    vat = models.CharField(max_length=25)
    
    # Specialization
    brand_type = models.CharField(choices=USERS, default='T', max_length=1)
    # ig_link = models.CharField(null=True, max_length=225)

    # Bank Details
    bank = models.CharField(choices=BANK, default='acc', max_length=3)
    account_number = models.CharField(max_length=25)
    account_name = models.CharField(max_length=255)

    def __str__(self):
        return self.business_name
    

def fabrics_image_path(instance, filename):
    return f'Fabric_{instance.partner.id}/fabric_images/images/{filename}'
class Fabric(models.Model):
    label = models.CharField(max_length=50, null=False)
    partner = models.ForeignKey(Partner, on_delete=CASCADE, null=False)    
    type = models.CharField(choices=FABRICS, default='K', max_length=1)
    price = models.IntegerField()
    per_yard = models.IntegerField("Minimum yard")
    image = models.ImageField(upload_to = fabrics_image_path)
    rating = models.IntegerField(choices=RATING, default=3)
    order_amount = models.IntegerField(default=1)

def cloth_image_path(instance, filename):
    return f'Partner_{instance.company.id}/clothes/images/{filename}'
class Cloth(models.Model):
    label = models.CharField("A lebel or identification title for this cloth sample", 
                              max_length=50, null=False)    
    company = models.ForeignKey(Partner, on_delete=CASCADE, null=False)
    price = models.IntegerField("Price of sample", default=1000)
    image = models.ImageField(upload_to = cloth_image_path)
    rating = models.IntegerField(choices=RATING, default=3)
    order_amount = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Clothes"
    
class CustomMadeCloth(models.Model):
    cloth_object = models.OneToOneField(Cloth, on_delete=CASCADE, null=False)
    category = MultiSelectField(max_length=2, choices=CUSTOMCLOTHES, default='MS',
                                       max_choices=10)

class SewedCloth(models.Model):
    cloth_object = models.OneToOneField(Cloth, on_delete=CASCADE, null=False)
    category = MultiSelectField(max_length=1, choices=CATEGORIES, default='M',
                                       max_choices=3)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=False)
    address = models.CharField(null=False, max_length=225)
    city = models.CharField(null=False, max_length=225)
    state = models.CharField(null=False, max_length=225)
    zipcode = models.CharField(null=True, max_length=225)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"



class FabricOrder(models.Model):
    order_id = models.CharField(max_length=255)
    order_item = models.ForeignKey(Fabric, on_delete=CASCADE, null=False)  
    order_customer = models.ForeignKey(Customer, on_delete=CASCADE, null=False)
    order_partner = models.ForeignKey(Partner, on_delete=CASCADE, null=False)    
    order_quantity = models.IntegerField('Quantity ordered', default=1)
    order_total_price = models.IntegerField('Total price', null=False)
    order_status = models.CharField(max_length=1, default='P', choices=STATUS)
    order_date = models.DateTimeField('Date ordered', default=datetime.now())

class CustomMadeOrder(models.Model):
    order_id = models.CharField(max_length=255)
    order_item = models.ForeignKey(Cloth, on_delete=CASCADE, null=False)  
    order_customer = models.ForeignKey(Customer, on_delete=CASCADE, null=False)
    order_partner = models.ForeignKey(Partner, on_delete=CASCADE, null=False)    
    order_quantity = models.IntegerField('Quantity ordered', default=1)
    order_total_price = models.IntegerField('Total price', null=False)
    order_status = models.CharField(max_length=1, default='P', choices=STATUS)
    order_date = models.DateTimeField('Date ordered', default=datetime.now())

class SewedClothOrder(models.Model):
    order_id = models.CharField(max_length=255)
    order_item = models.ForeignKey(Cloth, on_delete=CASCADE, null=False)  
    order_customer = models.ForeignKey(Customer, on_delete=CASCADE, null=False)
    order_partner = models.ForeignKey(Partner, on_delete=CASCADE, null=False)    
    order_quantity = models.IntegerField('Quantity ordered', default=1)
    order_total_price = models.IntegerField('Total price', null=False)
    order_status = models.CharField(max_length=1, default='P', choices=STATUS)
    order_date = models.DateTimeField('Date ordered', default=datetime.now())

class FabricSeller(models.Model):
    partner = models.OneToOneField(Partner, on_delete=CASCADE, null=False)
    specs = MultiSelectField(max_length=4, max_choices=4, choices=FABRICS)

class CustomMadeSeller(models.Model):
    partner = models.OneToOneField(Partner, on_delete=CASCADE, null=False)
    specs = MultiSelectField(max_length=4, max_choices=4, choices=CUSTOMCLOTHES)

class Tailor(models.Model):
    partner = models.OneToOneField(Partner, on_delete=CASCADE, null=False)
    specs = MultiSelectField(max_length=4, max_choices=4, choices=CATEGORIES)
    rating = models.IntegerField("tailor's rating", choices=RATING, default=3)
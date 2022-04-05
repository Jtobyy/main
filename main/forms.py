from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from multiselectfield.db.fields import MultiSelectField
from .models import Clothe, PendingTailorReg, PendingSellerReg
from django.contrib.auth.models import User

class RegForm(UserCreationForm):
    email = forms.EmailField(required=True)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        print(User.objects.values('email'))
        email = {'email': self.cleaned_data['email']}
        if email in User.objects.values('email'):
            return False
        user = super(RegForm, self).save(commit=True)
        user.email = self.cleaned_data['email']
        user.username = user.email
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class TailorRegForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TailorRegForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = PendingTailorReg
        fields = '__all__'
                 

class SellerRegForm(forms.ModelForm):
    class Meta:
        model = PendingSellerReg
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SellerRegForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
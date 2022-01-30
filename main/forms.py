from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from multiselectfield.db.fields import MultiSelectField
from .models import Clothe

class RegForm(UserCreationForm):
    email = forms.EmailField(required=True)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegForm, self).save(commit=True)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

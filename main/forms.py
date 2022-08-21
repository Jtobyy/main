from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cloth, Customer, PendingReg, FABRICS, CUSTOMCLOTHES, CATEGORIES
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Layout, Submit, Field, HTML
from crispy_forms.bootstrap import FormActions, AppendedText, PrependedText
from crispy_forms.bootstrap import PrependedAppendedText, InlineRadios, InlineCheckboxes

class RegForm(UserCreationForm):
    email = forms.EmailField(required=True)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        # print(User.objects.values('email'))
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

class PendingRegForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PendingRegForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta: 
        model = PendingReg
        fields = '__all__'


class FabricForm(forms.Form):
    label = forms.CharField(
        label="A lebel or identification title for this fabric",
        required=True
    )

    type = forms.TypedChoiceField(
        label="Type of fabric",
        choices=FABRICS,
        widget=forms.RadioSelect,
        initial='K',
        required=True,
    )

    per_yard = forms.IntegerField(
        label="Sold per how many yards",
        required=True,
    )

    price = forms.IntegerField(
        label="Price per yard",
        required=True,
    )
    
    image = forms.ImageField(allow_empty_file=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "idFabricForm"
        self.helper.form_method = "post"
        self.helper.form_action = "/main/addfabric"

        self.helper.layout = Layout(
            Field('label', css_class="form-control m-20", wrapper_class="form-group"),
            InlineRadios('type', wrapper_class="form-group"),
            AppendedText('per_yard', 'yard(s)', css_class="form-control", wrapper_class="input-group"),
            PrependedAppendedText('price', 'N', 'per yard', placeholder="1500", css_class="form-control",
            wrapper_class="form-group"),
            'image',
            'flag_featured',
            FormActions(
                Submit('Add', 'Add', css_class="btn btn-primary"),
            ),
        )


class CustomClothForm(forms.ModelForm):
    class Meta:
        model = Cloth
        fields = ('label', 'price', 'image')

    type = forms.MultipleChoiceField(
        label="Category of cloth sample",
        choices=CUSTOMCLOTHES,
        widget=forms.CheckboxSelectMultiple,
        initial='MS',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "idClothForm"
        self.helper.form_method = "post"
        self.helper.form_action = "/main/addcloth?type=custom"

        self.helper.layout = Layout(
            Field('label', css_class="form-control m-20", wrapper_class="form-group"),
            InlineCheckboxes('type', wrapper_class="form-group"),
            PrependedText('price', 'N', placeholder="2000", css_class="form-control",
            wrapper_class="form-group"),
            'image',
            'flag_featured',
            FormActions(
                Submit('Add', 'Add', css_class="btn btn-primary"),
            ),
        )


class SewedClothForm(forms.Form):
    label = forms.CharField(
        label="A lebel or identification title for this cloth sample",
        required=True
    )

    type = forms.MultipleChoiceField(
        label="Cloth sample category",
        choices=CATEGORIES,
        widget=forms.CheckboxSelectMultiple,
        initial='MS',
        required=True,
    )

    price = forms.IntegerField(
        label="Price of sample",
        required=True,
    )
    
    image = forms.ImageField(allow_empty_file=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "idClothForm"
        self.helper.form_method = "post"
        self.helper.form_action = "/main/addcloth?type=sewed"

        self.helper.layout = Layout(
            Field('label', css_class="form-control m-20", wrapper_class="form-group"),
            InlineCheckboxes('type', wrapper_class="form-group"),
        PrependedText('price', 'N', placeholder="1500", css_class="form-control",
            wrapper_class="form-group"),
            'image',
            'flag_featured',
            FormActions(
                Submit('Add', 'Add', css_class="btn btn-primary"),
            ),
        )

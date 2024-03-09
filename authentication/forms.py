from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            "class": "form-control"
        }))

    last_name = forms.CharField(required=True,  widget=forms.TextInput(
        attrs={
            "class": "form-control"
        }))
    username = forms.CharField(required=True,  widget=forms.TextInput(
        attrs={
            "class": "form-control"
        }))
    email = forms.EmailField(required=True,  widget=forms.TextInput(
        attrs={
            "class": "form-control"
        }))
    mobile_phone = forms.CharField(validators=[RegexValidator('^01[0-2,5]{1}[0-9]{8}$')], required=True,  widget=forms.TextInput(
        attrs={
            "class": "form-control"
        }))
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            "class": "form-control"
        }))
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={
        "class": "form-control"
    }))
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput(attrs={
        "class": "form-control"
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username' ,'email', 'mobile_phone', 'profile_picture', 'password1', 'password2']


    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        if not mobile_phone.startswith('01') or len(mobile_phone) != 11:
            raise forms.ValidationError('Please enter a valid Egyptian mobile phone number.')
        return mobile_phone

class LoginForm(forms.Form):
    username = forms.CharField(required=True,  widget=forms.TextInput(
        attrs={
            "class": "form-control"
        }))
    password = forms.CharField(required=True,  widget=forms.PasswordInput(
        attrs={
            "class": "form-control"
        }))
    


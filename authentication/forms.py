from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator, URLValidator
from .models import *
from django.core.exceptions import ValidationError





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
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={
        "class": "form-control"
    }))
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput(attrs={
        "class": "form-control"
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username' ,'email', 'mobile_phone', 'password1', 'password2']


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
    




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'birth_date', 'facebook', 'twitter', 'linkedin', 'bio']
        
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': ['form-control', 'form-control-file']}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_facebook(self):
        facebook = self.cleaned_data.get('facebook')
        if facebook:
            validate = URLValidator()
            try:
                validate(facebook)
            except ValidationError:
                raise ValidationError("Invalid Facebook URL")
        return facebook

    def clean_twitter(self):
        twitter = self.cleaned_data.get('twitter')
        if twitter:
            validate = URLValidator()
            try:
                validate(twitter)
            except ValidationError:
                raise ValidationError("Invalid Twitter URL")
        return twitter

    def clean_linkedin(self):
        linkedin = self.cleaned_data.get('linkedin')
        if linkedin:
            validate = URLValidator()
            try:
                validate(linkedin)
            except ValidationError:
                raise ValidationError("Invalid LinkedIn URL")
        return linkedin

    
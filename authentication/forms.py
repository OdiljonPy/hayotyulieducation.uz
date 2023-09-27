from django import forms
from django.contrib.auth.forms import UserCreationForm

from authentication.models import PersonInfo


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class PersonForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonInfo
        fields = [
            "first_name",
            "second_name",
            "father_name"
        ]


class FullPersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonInfo
        fields = [
            "first_name",
            "second_name",
            "father_name",
            "number_of_contract",
            "passport_serial_with_number",
            "study_major",
            "region",
            "school",
            "nationality"
        ]

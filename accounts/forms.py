from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    email = forms.EmailField(required=True)
    birth_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S'],
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime-local'}
        )
    )
    gender = forms.CharField(widget=forms.Textarea, required=False)
    address = forms.CharField(max_length=100, required=False)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'role', 'email', 'password1', 'password2', 'gender',
                  'address', 'phone')

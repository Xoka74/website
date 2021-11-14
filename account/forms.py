from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, EmailInput
from django.forms import TextInput, PasswordInput

User = get_user_model()


class UserLoginForm(Form):
    username = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'required': True}))
    password = CharField(widget=PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'required': True}))
    field_order = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    email = CharField(required=True)
    first_name = CharField(required=False)
    last_name = CharField(required=False)
    phone_number = CharField(required=False)
    field_order = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2


class UserEditForm(Form):
    use_required_attribute = False
    username = CharField(
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'required': False}))
    first_name = CharField(
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'required': False}))
    last_name = CharField(
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'required': False}))
    email = CharField(widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': False}))
    phone_number = CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number', 'required': False}))

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import Waste, ProfileImage


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))


class WasteForm(forms.ModelForm):
    class Meta:
        model = Waste
        fields = ('category',
                  'venue',
                  'title',
                  'unit',
                  'weight',)

        widgets = {
            'title': forms.TextInput(attrs={
                "id": "title",
                "class": "form-control",
                "placeholder": "Заголовок",
            }),

            'category': forms.Select(attrs={
                "id": "category",
                "class": "form-control",
            }),

            'venue': forms.Select(attrs={
                "id": "venue",
                "class": "form-control",
            }),

            'unit': forms.Select(attrs={
                "id": "unit",
                "class": "form-control",
            }),

            'weight': forms.NumberInput(attrs={
                "id": "weight",
                "class": "form-control",
                "placeholder": "Вес",
            }),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    widgets = {

        'username': forms.TextInput(attrs={
            "id": "username",
            "class": "form-control",
            "placeholder": "Имя пользователя",
        }),
        'email': forms.EmailInput(attrs={
            "id": "email",
            "class": "form-control",
            "placeholder": "Эл. почта",
        }),
        'password1': forms.PasswordInput(attrs={
            "id": "password1",
            "class": "form-control",
            "placeholder": "Пароль",
        }),
        'password2': forms.PasswordInput(attrs={
            "id": "password2",
            "class": "form-control",
            "placeholder": "Подтвердить пароль",
        }),
    }


# Create a UserUpdateForm to update a username and email
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        widgets = {
            'username': forms.TextInput(attrs={
                "id": "username",
                "class": "form-control",
                "placeholder": "Имя пользователя",
            }),
            'email': forms.EmailInput(attrs={
                "id": "email",
                "class": "form-control",
                "placeholder": "Эл. почта",
            }),
            'first_name': forms.TextInput(attrs={
                "id": "first_name",
                "class": "form-control",
                "placeholder": "Имя",
            }),
            'last_name': forms.TextInput(attrs={
                "id": "last_name",
                "class": "form-control",
                "placeholder": "Фамилия",
            }),
        }


# Create a ProfileUpdateForm to update image.
class ProfileImageUpdateForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                "id": "image",
                "class": "custom-file"
            })
        }

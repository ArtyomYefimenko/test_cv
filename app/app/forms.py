# -*- coding: utf-8 -*-
__author__ = 'artem'

from django import forms
from django.contrib.auth.forms import UserCreationForm
from my_user.models import MyUser
from django.forms.extras.widgets import SelectDateWidget
from captcha.fields import CaptchaField
from cv.models import User_CV


class RegistrationForm(UserCreationForm):
    captcha = CaptchaField()
    email = forms.EmailField(label='Email', max_length=75,
        widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "example@gmail.com"}))
    firstname = forms.CharField(required=True, label='Фамилия', max_length=75,
        widget=forms.TextInput(attrs={'class': "form-control"}))
    lastname = forms.CharField(required=True, label='Имя', max_length=75,
        widget=forms.TextInput(attrs={'class': "form-control"}))
    phone = forms.CharField(required=True, label='Номер телефона', max_length=75,
        widget=forms.TextInput(attrs={'class': "form-control phone", 'placeholder': "050-5555555"}))
    password1 = forms.CharField(min_length=6, max_length=16, label=("Пароль"),
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Введите пароль длиной от 6 до 12 символов"}))
    password2 = forms.CharField(min_length=6, max_length=16, label=("Пароль повторно"),
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Введите пароль повторно"}),
        help_text=("Введите повторно пароль"))
    date_of_birth = forms.DateField(required=True, label=("Дата рождения"),
        widget=SelectDateWidget(years=range(1950, 2016)))
    class Meta:
        model = MyUser
        fields = ('firstname', 'lastname', 'username', 'password1', 'password2', 'email', 'date_of_birth', 'phone')
        widgets = {
            'username': forms.TextInput(attrs={'class': "form-control"}),
        }


    def clean_email(self):

        email = self.cleaned_data["email"]
        try:
            user = MyUser.objects.get(email=email)
            raise forms.ValidationError("Этот адрес электронной почты уже занят")
        except MyUser.DoesNotExist:
            return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_active = True
        if commit:
            user.save()
        return user


class PrivateEditForm(forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=75,
        widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "example@gmail.com"}))
    firstname = forms.CharField(required=True, label='Фамилия', max_length=75,
        widget=forms.TextInput(attrs={'class': "form-control"}))
    lastname = forms.CharField(required=True, label='Имя', max_length=75,
        widget=forms.TextInput(attrs={'class': "form-control"}))
    phone = forms.CharField(required=True, label='Номер телефона', max_length=75,
        widget=forms.TextInput(attrs={'class': "form-control phone", 'placeholder': "050-5555555"}))
    password1 = forms.CharField(min_length=6, max_length=16, label=("Пароль"),
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Введите пароль длиной от 6 до 12 символов"}))
    password2 = forms.CharField(min_length=6, max_length=16, label=("Пароль повторно"),
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Введите пароль повторно"}),
        help_text=("Введите повторно пароль"))
    date_of_birth = forms.DateField(required=True, label=("Дата рождения"),
        widget=SelectDateWidget(years=range(1950, 2016)))
    class Meta:
        model = MyUser
        fields = ('firstname', 'lastname', 'username', 'password1', 'password2', 'email', 'date_of_birth', 'phone', 'avatar')
        widgets = {
            'username': forms.TextInput(attrs={'class': "form-control"}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароль и подтверждение не совпадают')
        return password2

    def save(self, commit=True):
        user = super(PrivateEditForm, self).save(commit=False)
        if user.set_password != self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_active = True
        if commit:
            user.save()
        return user


class UserAddCVForm(forms.ModelForm):
    class Meta:
        model = User_CV
        fields = ('cv',)
        widgets = {
            'cv': forms.FileInput(attrs={'accept': "application/pdf"}),
        }


class UserEditCVForm(forms.ModelForm):
    class Meta:
        model = User_CV
        fields = ('cv',)
        widgets = {
            'cv': forms.FileInput(attrs={'accept': "application/pdf"}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(required=True, label='Ваше имя', max_length=75,
        widget=forms.TextInput(attrs={'class': "form-control"}))
    subject = forms.CharField(required=True, label='Тема сообщения', max_length=75,
        widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(required=True, label='Email', max_length=75,
        widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "example@gmail.com"}))
    message = forms.CharField(required=True, label='Текст сообщения', max_length=500,
        widget=forms.Textarea(attrs={'class': "form-control"}))
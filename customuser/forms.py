# coding: utf-8
from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError


# # custom email validator
# def validate_email_unique(value):
#     users = get_user_model()
#     exists = users.objects.filter(email=value)
#     if exists:
#         raise ValidationError('this email already registered')
#
#
# class UserRegistrationForm(forms.ModelForm):
#     """
#     Form for registering a new account.
#     """
#
#     # Настройки для отображения полей формы
#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'E-mail Address'}),
#         label="Email",
#         validators=[validate_email_unique]
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),
#         label="Password"
#     )
#
#     # Указываем, какая модель используется для формы, и какой набор полей
#     class Meta:
#         model = get_user_model()
#         fields = ['email', 'password']
#
#     def clean_email(self):
#         data = self.cleaned_data['email']
#         validate_email(data)
#         return data
#
#     def clean_password(self):
#         data = self.cleaned_data['password']
#         validate_password(data)
#         return data
#
#     def save(self, commit=True):
#         user = super(UserRegistrationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#         return user

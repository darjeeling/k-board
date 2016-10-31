from django import forms
from django.contrib.auth import get_user_model

from registration.forms import RegistrationForm
from django_summernote import fields as summer_fields

from .models import SummerNote


class PostForm(forms.ModelForm):

     fields = summer_fields.SummernoteTextFormField(error_messages={'required':(u'데이터를 입력해주세요'),})
     class Meta:
           model = SummerNote
           fields = ('fields', )


class CustomRegistrationForm(forms.ModelForm):

    username = forms.CharField(
        label="ID"
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Password confirmation"
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'full_name', 'email', )

RegistrationForm.base_fields.update(CustomRegistrationForm.base_fields)
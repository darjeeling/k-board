from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from registration.forms import RegistrationForm
from django_summernote import fields as summer_fields

from .models import SummerNote


class PostForm(forms.ModelForm):

     fields = summer_fields.SummernoteTextFormField(error_messages={'required':(u'데이터를 입력해주세요'),})
     class Meta:
           model = SummerNote
           fields = ('fields', )


class CustomRegistrationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
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

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return make_password(password2)

    def clean(self):
        password = make_password(self.cleaned_data.get('password1'))
        self.cleaned_data['password'] = password

        if 'password1' in self.cleaned_data:
            del self.cleaned_data['password1']
        if 'password2' in self.cleaned_data:
            del self.cleaned_data['password2']
        return self.cleaned_data

RegistrationForm.base_fields.update(CustomRegistrationForm.base_fields)
from django import forms
from django.contrib.auth import get_user_model

from registration.forms import RegistrationForm
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote import fields as summer_fields

from .models import SummerNote
from .models import BoardUser


attrs_dict = { 'class': 'required' }

def affiliation_valid_email(value):
    allowed_domain = ['naver.com','gmail.com']
    #not the prettiest soliution
    v_error = ("Email does not match allowed domains (%s, %s)"
                           %(allowed_domain[0],allowed_domain[1]))
    if value.split('@')[1] not in allowed_domain:
        raise forms.ValidationError(v_error)
    else:
        return value


class PostForm(forms.ModelForm):

     fields = summer_fields.SummernoteTextFormField(error_messages={'required':(u'데이터를 입력해주세요'),})
     class Meta:
           model = SummerNote
           fields = ('fields', )


class CustomizeRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification."
    )

    class Meta:
        model = get_user_model()
        fields = (model.USERNAME_FIELD, ) + ('password1', 'password2', ) + tuple(model.REQUIRED_FIELDS)

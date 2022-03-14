from django import forms
from .models import UserDetails


class UserForm(forms.ModelForm):
    class Meta:
        re_password = forms.CharField(min_length=128, required = True, widget=forms.PasswordInput)
        model = UserDetails
        exclude = ['last_login']
        widgets = {
            're_password': forms.PasswordInput(),
        }
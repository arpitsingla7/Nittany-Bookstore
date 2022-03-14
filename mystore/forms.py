from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from mystore.models import registerdb
from django import forms

from mystore.models import registerdb

# UserCreationForm


class CreateUserForm(forms.ModelForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirm your password", widget=forms.PasswordInput)

    class Meta:
        model = registerdb
        fields = ['username', 'firstname', 'lastname',
                  'phone', 'address']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password does not match.")
        return password2

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.password(self.cleaned_data["password1"])
        # user.password1(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

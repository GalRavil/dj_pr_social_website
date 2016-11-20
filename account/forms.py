from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# Django provides similar form UserCreationForm (django.contrib.auth.forms)
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    # clean_<fieldname>() to clean the value or raise form validation error
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']


class UserEditForm(forms.ModelForm):
    """
    Will allow users to edit their first name, last name, and
    e-mail, which are stored in the built-in User model.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """
    Will allow users to edit the extra data we save in the custom Profile model.
    Users will be able to edit their date of birth and upload a picture for their profile.
    """
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')

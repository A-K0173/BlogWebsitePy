from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    """
    Form used to create a user from the User model.
    """

    # Manually add password field with PasswordInput widget
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
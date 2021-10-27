from django import forms
from django.core.exceptions import ValidationError
from .models import User

class RegistrationForm(forms.ModelForm):

    confirm = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'confirm', 'email')

    def clean_confirm(self):
        if self.cleaned_data['confirm']!=self.cleaned_data['password']:
            raise ValidationError("Parollar bir xil bo'lishi shart")

        return self.cleaned_data['confirm']

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ushbu foydalanuvchi oldin mavjud")
        return username


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'photo')

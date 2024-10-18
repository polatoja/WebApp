from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login 
from django import forms
from .models import Task
from .models import UserProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        label='Password'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email addresses must be unique. This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role='user')
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), label='Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='Password')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'level', 'due_date', 'assigned_user']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
        due_date = forms.DateField(input_formats=['%d-%m-%Y'])

    def save(self, commit=True):
        form = super().save(commit=False)
        if commit:
            form.save()
        return form
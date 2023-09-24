from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="username",
        min_length=5,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "flex h-10 w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
                "placeholder": "Enter Username",
            }
        ),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "flex h-10 w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
                "placeholder": "First Name",
            }
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "flex h-10 w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
                "placeholder": "Last Name",
            }
        ),
    )
    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput(
            attrs={
                "class": "flex h-10 w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
                "placeholder": "Email",
            }
        ),
    )
    password1 = forms.CharField(
        label="password",
        widget=forms.PasswordInput(
            attrs={
                "class": "flex h-10 w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
                "placeholder": "Enter Password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={
                "class": "flex h-10 w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
                "placeholder": "Confirm Password",
            }
        ),
    )

    def username_clean(self):
        username = self.cleaned_data["username"].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("User Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data["email"].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
        )
        return user

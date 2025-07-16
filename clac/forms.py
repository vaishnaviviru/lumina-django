from django import forms
from django.contrib.auth.models import User

from .models import Showcase


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@paycorp.local"):
            raise forms.ValidationError("Email must be @paycorp.local domain")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            self.add_error("confirm_password", "Passwords do not match")
        return cleaned_data


class ShowcaseForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = Showcase
        fields = ["title", "body_md", "link", "screenshot","email"    ]  # ✅ Removed 'attachment'

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title:
            raise forms.ValidationError("Title is required.")
        return title

    def clean_body_md(self):
        body = self.cleaned_data.get("body_md")
        if not body:
            raise forms.ValidationError("Body is required.")
        if len(body) < 10:
            raise forms.ValidationError("Body is too short.")
        return body

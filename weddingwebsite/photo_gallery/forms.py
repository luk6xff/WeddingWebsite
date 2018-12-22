#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from django import forms
from django.forms import CharField, Form, PasswordInput
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from .models import Album

from lockdown import settings

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = []

    zip = forms.FileField(required=False)


class LockdownPasswordForm(forms.Form):
    password = forms.CharField(label=mark_safe("<p> {} </p>".format(_('Please enter your password below'))), required=True, widget=PasswordInput(attrs={'placeholder': _('Password')}, render_value=False))

    def __init__(self, passwords=None, *args, **kwargs):
        """Initialize the form by setting the valid passwords."""
        super(LockdownPasswordForm, self).__init__(*args, **kwargs)
        if passwords is None:
            passwords = settings.PASSWORDS
        self.valid_passwords = passwords

    def clean_password(self):
        """Check that the password is valid."""
        value = self.cleaned_data.get('password')
        if value not in self.valid_passwords:
            raise forms.ValidationError('Incorrect password.')
        return value

    def generate_token(self):
        """Save the password as the authentication token.

        It's acceptable to store the password raw, as it is stored server-side
        in the user's session.
        """
        return self.cleaned_data['password']

    def authenticate(self, token_value):
        """Check that the password is valid.

        This allows for revoking of a user's preview rights by changing the
        valid passwords.
        """
        return token_value in self.valid_passwords

    def show_form(self):
        """Show the form if there are any valid passwords."""
        return bool(self.valid_passwords)
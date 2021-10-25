# -*- encoding: utf-8 -*-
from django.forms import CharField, PasswordInput, Form, HiddenInput, ValidationError
import re
class PasswordChangeForm(Form):
    error_messages = {'password_mismatch': "The two password fields didn't match."}
    password = CharField(label="password", widget=PasswordInput)
    rpassword = CharField(label="New password confirmation", widget=PasswordInput)
    username = CharField(widget=HiddenInput())

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.search(r"(?=.*[A-Z]+.*)", password):
            raise ValidationError(
                'Must contain a uppercase letter',
                code="password_letter"
            )
        if not re.search(r"(?=.*[0-9]+.*)", password):
            raise ValidationError(
                'Must contain a number',
                code="password_number"
            )
        if re.search(r"(?=.*[\s]+.*)", password):
            raise ValidationError(
                'Must not contain space',
                code="password_space"
            )
        if len(password) < 8:
            raise ValidationError(
                'Must contain more that seven characters',
                code="password_len"
            )
        return password

    def clean_rpassword(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('rpassword')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            else:
                return password2

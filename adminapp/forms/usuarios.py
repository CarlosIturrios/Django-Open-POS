from __future__ import unicode_literals
import uuid

from django.contrib.auth import password_validation
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Contraseña confirmación',
        widget=forms.PasswordInput,
        strip=False,
        help_text='Introduzca la misma contraseña que antes, para la verificación.',
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Los dos campos de contraseña no coinciden.',
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('email')
        password_validation.validate_password(
            self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        user.codigo_invitacion = str(uuid.uuid4()).upper()
        if commit:
            user.save()
            my_group = Group.objects.get(name='ADMINISTRADOR')
            my_group.user_set.add(user)

        return user


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email',)

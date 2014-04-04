from django.core.exceptions import ValidationError
from django.http import request

__author__ = 'Aaron'

from django import forms
from django.forms import BaseModelForm
from django.contrib.auth.models import User
from tickets.models import StaffMember
from django.core import validators
import re
from django.utils.translation import ugettext_lazy as _

class StaffMemberForm(forms.ModelForm):
    username = forms.CharField(label=_('Username'))
    first_name = forms.CharField(label=_('First name'))
    last_name = forms.CharField(label=_('Last name'))
    email = forms.EmailField(label=_('Email'))
    class Meta:
        model = StaffMember
        fields = ['staff_type', 'user']

    def clean(self):
        elif
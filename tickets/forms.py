__author__ = 'Aaron'

from django import forms
from django.contrib.auth.models import User
from tickets.models import StaffMember
from django.utils.translation import ugettext_lazy as _


class StaffMemberForm(forms.ModelForm):
    user = forms.ModelChoiceField(User.objects.all(), label=_('User'), required=False)
    username = forms.CharField(label=_('Username'), required=False)
    first_name = forms.CharField(label=_('First name'), required=False)
    last_name = forms.CharField(label=_('Last name'), required=False)
    email = forms.EmailField(label=_('Email'), required=False)

    class Meta:
        model = StaffMember
        fields = ('staff_type',)

    def clean(self):
        super(StaffMemberForm, self).clean()
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        email = cleaned_data.get("email")
        user = cleaned_data.get("user")
        staff_type = cleaned_data.get("staff_type")
        check = [username, user]
        if staff_type:
            if any(check) and not all(check):
                return cleaned_data
        raise forms.ValidationError(_('Choose a user from the dropdown or make a new user'))
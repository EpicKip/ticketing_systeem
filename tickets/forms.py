__author__ = 'Aaron'

from django import forms
from django.contrib.auth.models import User
from tickets.models import StaffMember
from django.utils.translation import ugettext_lazy as _
import uuid


class StaffMemberForm(forms.ModelForm):
    user = forms.ModelChoiceField(User.objects.all(), label=_('User'), required=False)
    username = forms.CharField(label=_('Username'), required=False)
    first_name = forms.CharField(label=_('First name'), required=False)
    last_name = forms.CharField(label=_('Last name'), required=False)
    email = forms.EmailField(label=_('Email'), required=False)

    @staticmethod
    def password_random(string_length):
        random = str(uuid.uuid4())
        random = random.upper()
        random = random.replace("-", "")
        return random[0:string_length]

    class Meta:
        model = StaffMember
        fields = ('staff_type',)

    def clean(self):
        if self.errors:
            return self.cleaned_data

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
        raise forms.ValidationError(_('Choose a user from the dropdown OR make a new user'))

    def save(self, commit=True):
        # Run the default save method, commit=False stops the
        # model saving to the db
        staff_member = super(StaffMemberForm, self).save(commit=False)

        if self.cleaned_data.get("user") is None:
            # Create a new User object
            user = User.objects.create_user(
                self.cleaned_data['username'],
                self.cleaned_data['email'],
                self.password_random(8)
            )
            print(self.password_random(7))
            # user.username = self.cleaned_data['username']
            # user.first_name = self.cleaned_data['first_name']
            # user.last_name = self.cleaned_data['last_name']
            # user.email = self.cleaned_data['email']
            # user.password = self.password_random(8)
            #
            # # Save new user
            user.save()

            print(user.id)
            assert False
            # Apply the new user to the staff_member object
            staff_member = user

        else:
            staff_member.user = self.cleaned_data.get("user")

        # If the form was expecting to save the StaffMember then save
        if commit:
            staff_member.save()
        return self
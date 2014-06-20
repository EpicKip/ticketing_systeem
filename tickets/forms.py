__author__ = 'Aaron'

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import make_password

from tickets.models import StaffMember
from utils import password_random


class StaffMemberForm(forms.ModelForm):
    """
        This makes new fields in the Staffmember section of the admin panel, these new fields will
        be used to create a user to be assigned staff member in case the new staff member is no user yet
    """
    user = forms.ModelChoiceField(User.objects.all(), label=_('User'), required=False)
    username = forms.CharField(label=_('Username'), required=False)
    first_name = forms.CharField(label=_('First name'), required=False)
    last_name = forms.CharField(label=_('Last name'), required=False)
    email = forms.EmailField(label=_('Email'), required=False)

    class Meta:
        """
            The model is defined and what fields to use from the model
        """
        model = StaffMember
        fields = ('staff_type', 'event')

    def clean(self):
        # All fields are checked for errors like:
        # Does a user exist already, did they fill in required fields and did they leave fields empty if they
        # chose a user from the drop down menu
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
                if user is None:
                    #If email field is not empty
                    if email:
                        #Check if user exists
                        try:
                            User.objects.get(username=username)
                        except User.DoesNotExist:
                            #if it does not, return user data
                            return cleaned_data
                        else:
                            #If username exists in database
                            raise forms.ValidationError(_('The desired username is already in use'))
                    elif email is u'':
                        #if email is empty
                        raise forms.ValidationError(_('You have to provide an email address if you make a new user'))
                else:
                    if email is u'' and first_name is u'' and last_name is u'':
                        #Checking for data in fields that require to be empty
                        return cleaned_data
                    else:
                        raise forms.ValidationError({'email': [_("You can\'t edit users from the list box")]})
            else:
                #Checking if any of the 2 options are selected but not both
                raise forms.ValidationError(_('Choose a user from the list box OR make a new user'))

    def save(self, commit=True):
        # Run the default save method, commit=False stops the
        # model saving to the db
        staff_member = super(StaffMemberForm, self).save(commit=False)
        staff_member.the_password = None

        if self.cleaned_data.get("user") is None:
            # Create a new User object
            user = User()
            user.username = self.cleaned_data['username']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            the_password = password_random(8)
            staff_member.the_password = the_password
            encrypted_password = make_password(the_password)
            user.password = encrypted_password
            # Save new user
            user.save()
            # Apply the new user to the staff_member object
            staff_member.user = user

            # body =      _('Dear user, someone has created an account for you at'
            # ' the nation events ticketing admin panel.\n'
            # 'They assigned you staff at one of their events.\n'
            # 'Here is your username and password:\n'
            #             'Username: %s\n'
            #             'Password: %s'
            #             % (user.username, the_password))
            # recipient = '%s' % user.email
            #
            # send_mail(_('Account created'), body, 'Ticketing@Nationevents.nl', [recipient])
        else:
            staff_member.user = self.cleaned_data.get("user")

        # If the form was expecting to save the StaffMember then save
        if commit:
            staff_member.save()
        return staff_member



__author__ = 'Aaron'

from django.forms import *
from django.contrib.auth.models import User
from tickets.models import *


class UserModelChoiceField():
    def label_from_instance(self, obj):
        return (obj.username)


class StaffMemberForm(ModelForm):
    # username = User.username
    # first_name = User.first_name
    # last_name = User.last_name
    # email = User.email
    username = UserModelChoiceField(User.objects.all().order_by('username'))
    class Meta:
        model = StaffMember
__author__ = 'aaron'

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

STAFF_TYPES = (
    ('OG', _('Organizer')),
    ('MO', _('Moderator')),
    ('SC', _('Scanner'))
)


class Customer(models.Model):
    """
        Customer class
    """
    user = models.OneToOneField(
        User,
        verbose_name=_('user'))

    @property
    def full_name(self):
        # try:
        if self.user.first_name or self.user.last_name:
            full = self.user.first_name + " " + self.user.last_name
        else:
            full = "(" + str(self.user) + ")"
        # except AttributeError:
        #     full = "ErrorName"
        return unicode(full)

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')

    def __str__(self):
        return self.user.username


class Event(models.Model):
    """
        Event class
    """
    name = models.CharField(max_length=100, verbose_name=_('name'))
    location = models.CharField(max_length=200, verbose_name=_('location'))
    start_time = models.DateTimeField(verbose_name=_('start time'))
    end_time = models.DateTimeField(verbose_name=_('end time'))
    sales_start = models.DateField(verbose_name=_('sales start'))
    sales_end = models.DateField(verbose_name=_('sales end'))
    event_active = models.BooleanField(verbose_name=_('event active'))
    information = models.CharField(max_length=500, verbose_name=_('information'))
    logo = models.ImageField(verbose_name=_('logo'), blank=True, upload_to='img/%Y/%m/%d')
    template = models.FileField(verbose_name=_('ticket template'), blank=True, upload_to='template/' + str(id))

    def clean(self):
        if self.sales_start > self.sales_end:
            raise ValidationError(_('The start of the sales can\'t be after the end...'))
        if self.start_time > self.end_time:
            raise ValidationError(_('The start of the event can\'t be after the end...'))
        if self.start_time.date() < self.sales_end:
            raise ValidationError(_('The sales can\'t end more then a day after the event itself...'))

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')


class EventTicket(models.Model):
    """
        Event ticket class (different kind of tickets per event)
    """
    name = models.CharField(max_length=100, verbose_name=_('name'))
    event = models.ForeignKey('Event', verbose_name=_('event'))
    price = models.FloatField(verbose_name=_('price'))
    maximum = models.IntegerField(verbose_name=_('maximum'))
    info = models.CharField(max_length=500, verbose_name=_('information'))


class Ticket(models.Model):
    """
        Ticket class
    """

    ticket_active = models.BooleanField(verbose_name=_('ticket active'))
    customer = models.ForeignKey('Customer', verbose_name=_('customer'))
    event = models.ForeignKey('EventTicket', verbose_name=_('event ticket'))

    def __unicode__(self):
        return unicode(self.id)

    class Meta:
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')

    @property
    def full_name(self):
        # try:
        if self.user.first_name or self.user.last_name:
            full = self.user.first_name + " " + self.user.last_name
        else:
            full = "(" + str(self.user) + ")"
        # except AttributeError:
        #     full = "ErrorName"
        return unicode(full)


class StaffMember(models.Model):
    """
        Staff member class
    """

    user = models.ForeignKey(User, verbose_name=_('user'), blank=True, null=True)
    event = models.ForeignKey(Event, verbose_name=_('event'))
    staff_type = models.CharField(
        max_length=3,
        choices=STAFF_TYPES,
        verbose_name=_('staff type')
    )

    @property
    def full_name(self):
        try:
            if self.user.first_name or self.user.last_name:
                full = self.user.first_name + " " + self.user.last_name
            else:
                full = "(" + str(self.user) + ")"
        except AttributeError:
            full = "ErrorName"
        return unicode(full)

    def __unicode__(self):
        return self.full_name

    class Meta:
        verbose_name = _('staff member')
        verbose_name_plural = _('staff members')

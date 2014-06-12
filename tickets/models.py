from django.core.files.storage import FileSystemStorage

__author__ = 'aaron'

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

# These are all the staff types and Payment statuses, the word after the comma is what you will see in the admin panel,
# but the text on the left is how it will be saved in the database
STAFF_TYPES = (
    ('OG', _('Organizer')),
    ('MO', _('Moderator')),
    ('SC', _('Scanner'))
)

PAYMENT_STATUS = (
    ('OPE', _('open')),
    ('CAN', _('cancelled')),
    ('PAI', _('paid')),
    ('PAO', _('paidout')),
    ('REF', _('refunded')),
    ('EXP', _('expired'))
)

fs = FileSystemStorage(location=settings.PDF_LOCATION)


class Customer(models.Model):
    """
        Customer class
            Customer has a 1 to 1 relationship with user
            It also has a property full_name, this is used in the admin dashboard
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
        return unicode(full)

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')

    def __str__(self):
        return self.user.username


class Event(models.Model):
    """
        Event class
            Event has a lot of time related fields such as:
                start/end_time  - The time the event starts/ends
                sales_start/end - The time the sales start/end

            Event has to be active too, this is done with the BooleanField: event_active
            The clean method is the validation, it returns errors to the user when you don't pass validation.
    """
    name = models.CharField(max_length=100, verbose_name=_('name'))
    location = models.CharField(max_length=200, verbose_name=_('location'))
    start_time = models.DateTimeField(verbose_name=_('start time'))
    end_time = models.DateTimeField(verbose_name=_('end time'))
    event_active = models.BooleanField(verbose_name=_('event active'))
    information = models.CharField(max_length=500, verbose_name=_('information'))
    logo = models.ImageField(verbose_name=_('logo'), blank=True, upload_to='img/%Y/%m/%d')
    template = models.FileField(verbose_name=_('ticket template'), blank=True, upload_to='template/%Y/%m/%d')

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError(_('The start of the event can\'t be after the end...'))

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')


class EventTicket(models.Model):
    """
        Event ticket class
            Every event has multiple kinds of tickets,
            example: normal tickets and v.i.p. tickets
    """
    name = models.CharField(max_length=100, verbose_name=_('name'))
    event = models.ForeignKey('Event', verbose_name=_('event'))
    price = models.FloatField(verbose_name=_('price'))
    maximum = models.IntegerField(verbose_name=_('maximum'))
    info = models.CharField(max_length=500, verbose_name=_('information'))

    def __unicode__(self):
        return unicode(self.id)

    class Meta:
        verbose_name = _('ticket type')
        verbose_name_plural = _('ticket types')


class Ticket(models.Model):
    """
        Ticket class
            Every ticket is active (scanned) connected to a certain type (wich is connected to an Event)
            and has a certain order Nr.
    """

    ticket_active = models.BooleanField(default=False, verbose_name=_('ticket active'))
    ticket_type = models.ForeignKey('EventTicket', verbose_name=_('ticket type'))
    order = models.ForeignKey('Order', verbose_name=_('order'))

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


class Order(models.Model):
    """
        Order class
            Every time you order tickets they will connect to an Order, this order contains the total price and
            tells you wich tickets you bought and how many of them
    """
    first_name = models.CharField(max_length=200, verbose_name=_('first name'))
    last_name = models.CharField(max_length=200, verbose_name=_('last name'))
    email = models.EmailField(verbose_name=_('email'))
    date_time = models.DateTimeField(verbose_name=_('date time'))
    payment_status = models.CharField(max_length=3, choices=PAYMENT_STATUS, verbose_name=_('payment status'))
    raw_order = models.TextField(verbose_name=_('raw order'))
    total = models.FloatField(verbose_name=_('total'))
    pdf = models.FileField(blank=True, null=True, upload_to='pdf', storage=fs, verbose_name=_('pdf'))

    def __unicode__(self):
        return unicode(self.id)


class StaffMember(models.Model):
    """
        Staff member class
            Staff member has a user connected to it, an event and a staff type
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


class Terms(models.Model):
    """
        You can save the terms and conditions here
    """
    terms = models.TextField(max_length=300, verbose_name=_('terms'))


class Mollie_key(models.Model):
    """
        You can save the terms and conditions here
    """
    key = models.CharField(max_length=300, verbose_name=_('terms'))


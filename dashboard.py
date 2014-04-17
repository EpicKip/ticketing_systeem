"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'ticketing.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import modules, Dashboard


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    
    def init_with_context(self, context):
        # append an app list module for "Ticketing"
        self.children.append(modules.ModelList(
            _('Ticketing'),
            collapsible=True,
            column=1,
            exclude=('django.contrib.*', 'tickets.models.Customer'),
            models=('tickets.models.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('Users'),
            column=1,
            collapsible=True,
            css_classes=('grp-closed',),
            models=('django.contrib.auth.models.User', 'tickets.models.Customer'),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent changes'),
            limit=5,
            collapsible=False,
            column=3,
        ))
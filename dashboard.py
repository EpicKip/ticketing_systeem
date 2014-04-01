"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'ticketing.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # append an app list module for "Ticketing"
        self.children.append(modules.ModelList(
            _('Ticketing'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            exclude=('django.contrib.*',),
            models=('tickets.models.*'),
        ))
        
        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('Users'),
            column=1,
            collapsible=False,
            models=('django.contrib.auth.models.User',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent changes'),
            limit=5,
            collapsible=False,
            column=3,
        ))




__author__ = 'Aaron'

DEVELOPMENT_MACHINES = ('PETERPC', 'Harry')
TESTING_MACHINES = ('ip-10-227-39-94',)
PRODUCTION_MACHINES = ('ip-10-48-199-83',)

import os
import platform
import sys
import warnings

from django.utils.importlib import import_module
pdflocation = ''


def get_server_name():
    server_type = os.environ.get('SERVER_TYPE', '')
    server_name = platform.node().split('.')[0]
    if server_type:
        return server_type
    if server_name in DEVELOPMENT_MACHINES:
        if server_name == 'PETERPC' or 'Harry':
            return 'settings_aaron'
    if server_name in TESTING_MACHINES:
        return 'testing'
    if server_name in PRODUCTION_MACHINES:
        return 'prod'
    else:
        return server_name


def override_settings(dottedpath):
    sys.path.append(os.sep.join(os.path.abspath(os.path.dirname(__file__)).split(os.sep)[:-1]))

    try:
        _module = import_module(dottedpath)
    except ImportError, e:
        warnings.warn("Failed to import %s" % dottedpath)
        warnings.warn("Exact error was: %s" % e)
    else:
        _thismodule = sys.modules[__name__]
        for _keyword in dir(_module):
            if _keyword.isupper() and not _keyword.startswith('__'):
                setattr(_thismodule, _keyword, getattr(_module, _keyword))

override_settings('ticketing_systeem.base')
override_settings('ticketing_systeem.%s' % get_server_name())
#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import logging, logging.handlers
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from rapidsms.backends.base import BackendBase



class Command(BaseCommand):
    help = "Starts the given backend.  E.g., ./manage.py runbackend pygsm"
    args = "<backend>"
    
    def handle(self, *args, **kwargs):
        if len(args) != 1:
            raise CommandError("You must specify exactly one backend.")
        backend = args[0]
        
        if backend not in settings.INSTALLED_BACKENDS:
            raise CommandError("Backend '%s' not found in INSTALLED_BACKENDS" %
                               backend)
        
        logger = logging.getLogger()
        numeric_level = getattr(logging, settings.LOG_LEVEL.upper())
        format = logging.Formatter(settings.LOG_FORMAT)

        # start logging to the screen (via stderr)
        # TODO: allow the values used here to be
        # specified as arguments to this command
        handler = logging.StreamHandler()
        handler.setLevel(numeric_level)
        handler.setFormatter(format)
        
        # start logging to file
        file_handler = logging.handlers.RotatingFileHandler(
            settings.LOG_FILE, maxBytes=settings.LOG_SIZE,
            backupCount=settings.LOG_BACKUPS)
        file_handler.setFormatter(format)

        logger.setLevel(numeric_level)
        logger.addHandler(handler)
        #logger.addHandler(file_handler)
        
        # update the persistance models. (this is not djangonic at all.
        # it should be replaced with managers for App and Backend.)
        call_command("update_backends", verbosity=0)
        call_command("update_apps", verbosity=0)

        module_name = settings.INSTALLED_BACKENDS[backend].pop("ENGINE")
        config = settings.INSTALLED_BACKENDS[backend] or {}
        cls = BackendBase.find(module_name)
        if cls is None:
            raise CommandError("Backend module '%s' not found." % module_name)
        backend = cls(backend, **config)
        backend.start()

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


# noinspection PyRedeclaration
class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        import app.signals

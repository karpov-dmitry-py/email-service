# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Topic
from .models import Customer
from .models import NewsLetter
from .models import Tracking

admin.site.register(Topic)
admin.site.register(Customer)
admin.site.register(NewsLetter)
admin.site.register(Tracking)

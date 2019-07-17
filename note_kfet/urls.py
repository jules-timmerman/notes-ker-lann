# -*- mode: python; coding: utf-8 -*-
# Copyright (C) 2018-2019 by BDE ENS Paris-Saclay
# SPDX-License-Identifier: GPL-3.0-or-later

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Dev so redirect to something random
    path('', RedirectView.as_view(pattern_name='note:transfer'), name='index'),

    # Include project routers
    path('note/', include('note.urls')),

    # Include Django Contrib and Core routers
    # admin/login/ is redirected to the non-admin login page
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/',
         RedirectView.as_view(pattern_name='index')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
]

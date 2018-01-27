# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

from .forms import LoginForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(form_class=LoginForm)),
    url(r'^', include('documents.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
    ]
    urlpatterns += staticfiles_urlpatterns()

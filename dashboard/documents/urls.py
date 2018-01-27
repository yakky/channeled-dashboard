# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import url

from .views import DocumentCreate, DocumentDetail, DocumentList, DocumentUpdate

urlpatterns = [
    url('^add/$', DocumentCreate.as_view(), name='document-create'),
    url('^(?P<slug>[^/]+)/update/$', DocumentUpdate.as_view(), name='document-update'),
    url('^(?P<slug>[^/]+)/$', DocumentDetail.as_view(), name='document-detail'),
    url('^$', DocumentList.as_view(), name='documents-list')
]

# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.urls import path

from .views import DocumentCreate, DocumentDetail, DocumentList, DocumentUpdate

urlpatterns = [
    path('add/', DocumentCreate.as_view(), name='document-create'),
    path('<str:slug>/update/', DocumentUpdate.as_view(), name='document-update'),
    path('<str:slug>/', DocumentDetail.as_view(), name='document-detail'),
    path('', DocumentList.as_view(), name='documents-list')
]

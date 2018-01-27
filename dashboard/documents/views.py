# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import DocumentForm
from .models import Document


class DocumentList(LoginRequiredMixin, ListView):
    model = Document
    context_object_name = 'documents'


class DocumentCreate(LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    context_object_name = 'document'

    def get_form_kwargs(self):
        kwargs = super(DocumentCreate, self).get_form_kwargs()
        kwargs['author'] = self.request.user.pk
        return kwargs


class DocumentUpdate(LoginRequiredMixin, UpdateView):
    model = Document
    context_object_name = 'document'
    form_class = DocumentForm

    def get_success_url(self):
        return reverse('document-update', kwargs={'slug': self.object.slug})


class DocumentDetail(LoginRequiredMixin, DetailView):
    model = Document
    context_object_name = 'document'

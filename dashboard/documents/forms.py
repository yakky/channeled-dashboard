# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django import forms

from dashboard.forms import BulmaMixin

from .models import Document


class DocumentForm(BulmaMixin, forms.ModelForm):
    author = None

    class Meta:
        model = Document
        fields = ['title', 'image', 'abstract', 'text']

    def __init__(self, *args, **kwargs):
        self.setup_widgets()
        self.author = kwargs.pop('author', None)
        super(DocumentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if self.author and not self.instance or not self.instance.author_id:
            self.instance.author_id = self.author
        return super(DocumentForm, self).save(commit)

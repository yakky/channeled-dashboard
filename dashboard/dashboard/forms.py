# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django import forms
from django.contrib.auth.forms import AuthenticationForm


class BulmaMixin(object):
    base_fields_classes = {
        forms.TextInput: 'input',
        forms.PasswordInput: 'input',
        forms.ClearableFileInput: 'file-input',
        forms.Textarea: 'textarea'
    }
    templates = {
        forms.ClearableFileInput: 'documents/includes/clearable_file_input.html',
    }

    def setup_widgets(self):
        for field in self.base_fields:
            widget = self.base_fields[field].widget
            css_class = self.base_fields_classes.get(widget.__class__, None)
            if css_class:
                self.base_fields[field].widget.attrs['class'] = css_class
            template = self.templates.get(widget.__class__, None)
            if template:
                self.base_fields[field].widget.template_name = template


class LoginForm(BulmaMixin, AuthenticationForm):

    def __init__(self, *args, **kwargs):
        self.setup_widgets()
        super(LoginForm, self).__init__(*args, **kwargs)

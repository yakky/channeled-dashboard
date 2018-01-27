# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    date_hierarchy = 'created'

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author_id = request.user.pk
        return super(DocumentAdmin, self).save_model(request, obj, form, change)

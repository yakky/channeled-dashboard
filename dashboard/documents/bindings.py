# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from channels.binding.websockets import WebsocketBinding

from .models import Document


class DocumentBinding(WebsocketBinding):
    # Document linked to the binder
    model = Document
    # Name of the stream: must be matched in the js code
    stream = 'document'
    # Fields sent to the frontend on update
    # more complex serialization requires overriding the `serialize_data`
    # method
    fields = ['title', 'image', 'abstract', 'text', 'author', 'slug']

    @classmethod
    def group_names(cls, instance):
        """
        Group names the receive notifications, must be included in multiplexer groups
        """
        return ['notifications']

    def has_permission(self, user, action, pk):
        """
        Authorization logic to allow / restrict actions (create, update or delete)
        """
        return user.is_authenticated

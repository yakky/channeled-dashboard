# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from documents.routing import channel_routing as documents_routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            # This only works on channels 2.1
            # andrew won't probably super-like this
            path('status/', documents_routing),
        ])
    ),
})

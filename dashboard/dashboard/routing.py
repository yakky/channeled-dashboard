# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from knocker.routing import channel_routing as knocker_routing

from documents.routing import channel_routing as documents_routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('status/', documents_routing),
            path('knocker/', knocker_routing),
        ])
    ),
})

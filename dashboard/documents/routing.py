# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from channels import route_class

from .consumers import Demultiplexer, DocumentDetailStatusConsumer, DocumentListStatusConsumer, UserCounterConsumer

# consumers can be freely appended: path (and other filters) ensure the
# correct match
# No channel is declared, as they are declared in the parent class (WebsocketConsumer)
channel_routing = [
    UserCounterConsumer.as_route(path=r'/users/'),
    DocumentListStatusConsumer.as_route(path=r'/documents/'),
    DocumentDetailStatusConsumer.as_route(path=r'/document/(?P<slug>[^/]+)/(?P<phase>[^/]+)/'),
    # route_class is the channel API, while `as_route` is a method specific to parent BaseConsumer
    # as_route internally uses route_class anyway, thus it's just a matter of style
    route_class(Demultiplexer, path=r'/notifications/'),
]

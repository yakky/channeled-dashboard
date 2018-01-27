# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from channels.routing import include

from documents.routing import channel_routing as documents_routing

# equivalent to my_project.urls
# tipically used to include application routing
channel_routing = [
    include(documents_routing, path=r'^/status'),
]

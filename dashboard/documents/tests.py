# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from channels.test import ChannelTestCase, WSClient


class DocumentConsumerTest(ChannelTestCase):

    def test_connect(self):
        client = WSClient()

        client.send_and_consume('websocket.connect', path='/status/users/')
        self.assertEqual(client.receive(), {'users': 0})

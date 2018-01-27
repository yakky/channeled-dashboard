# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from channels.generic.websockets import JsonWebsocketConsumer, WebsocketDemultiplexer
from django.core.cache import cache

from .bindings import DocumentBinding
from .models import Document


class UserCounterConsumer(JsonWebsocketConsumer):
    """
    This consumer is responsible for registering all the currently active users
    to send them generic notifications

    We rely on base class `method_mapping` that maps channels to methods::

        method_mapping = {
            "websocket.connect": "raw_connect",
            "websocket.receive": "raw_receive",
            "websocket.disconnect": "raw_disconnect",
        }

    WebsocketConsumer provides a higher level of abstraction by exposing
    `connect`, `disconnect`, `receive` which handles message encoding / decoding.

    We don't need to handle incoming messages, thus the `received` method is not
    implemented.
    """
    # Keep track of the current Django user across all the states
    channel_session_user = True
    http_user = True

    # local shortcut
    users_group = 'users'

    def connection_groups(self, **kwargs):
        """
        This consumer will be attached to the general users group

        We want to send messages regarding the documents changes and
        the number of connected users at different times, thus we use
        different groups
        """
        return self.users_group,

    def _notify_user_counter(self):
        """
        Counts the users in cache and send the message to the whole group::

            {
                'users': '<number-of-users>'
            }
        """
        msg = {
            self.users_group: len(cache.get(f'documents-{self.users_group}', {})),
        }
        self.group_send(self.users_group, msg)

    def connect(self, message, **kwargs):
        """
        On connect, we count the user as online and we send back the number
        of users currently online.

        Users are counted by saving keeping id/username in a cache dictionary.
        """
        super(UserCounterConsumer, self).connect(message, **kwargs)
        if message.user.is_authenticated:
            # let's ignore possible race conditions here :)
            data = cache.get(f'documents-{self.users_group}', {})
            data[message.user.pk] = message.user.get_full_name()
            cache.set(f'documents-{self.users_group}', data)
        self._notify_user_counter()

    def disconnect(self, message, **kwargs):
        """
        On disconnect, the user is removed
        """
        if message.user.is_authenticated:
            data = cache.get(f'documents-{self.users_group}', {})
            data.pop(message.user.pk, None)
            cache.set(f'documents-{self.users_group}', data)
        self._notify_user_counter()
        super(UserCounterConsumer, self).disconnect(message, **kwargs)


class DocumentListStatusConsumer(JsonWebsocketConsumer):
    """
    This provides the status of each document with the list of attached users and their phases

    When a client connects, an update is sent to all the connected clients to inform them
    about the document statuses
    """
    # Keep track of the current Django user across all the states
    channel_session_user = True
    http_user = True

    # we track these two document states
    phases = [Document.Status.read, Document.Status.update]

    def connection_groups(self, **kwargs):
        """
        Attached do the documents list group
        """
        return [Document.Status.list]

    def notify_documents(self):
        """
        The list of users in each phase of each document is sent to the list group
        """
        statuses = {}
        for document in Document.objects.all().values_list('slug', flat=True):
            statuses[document] = {
                phase: cache.get(Document.cache_key(document, phase), {}) for phase in self.phases
            }
            statuses[document]['document'] = document
        self.group_send(Document.Status.list, statuses)

    def connect(self, message, **kwargs):
        """
        Send the the status of all the documents (i.e: the list of connected users for each document/phase) to the
        generic group
        """
        super(DocumentListStatusConsumer, self).connect(message, **kwargs)
        self.notify_documents()


class DocumentDetailStatusConsumer(DocumentListStatusConsumer):
    """
    This consumer tracks the status of the different documents.

    When a user connect/disconnect, a frame is sent to all the clients, both the ones connected to the specific
    document, and the ones on the list of documents

    Is attached to a route without a slug, it will reports the status of all the documents
    """

    def connection_groups(self, **kwargs):
        """
        If consumer is attached to a document, is registered on the document-specific group
        """
        return [self.kwargs.get('slug'), Document.Status.list]

    def notify_current_document(self):
        """
        The numbers of users in each of the current document phases is sent to all the groups of the current document
        """
        statuses = {
            phase: cache.get(Document.cache_key(self.kwargs['slug'], phase), {}) for phase in self.phases
        }
        statuses['document'] = self.kwargs['slug']
        self.group_send(self.kwargs.get('slug'), statuses)

    def connect(self, message, **kwargs):
        """
        When opening the detail / form, the current user is assigned to the correct phase, then
        the users connected to the list received all the documents statuses while the ones connected
        to the current document are updated about it
        """
        # kwargs contains the routing filter parameters
        # {'slug': <document-slug>, 'phase': 'read|update'}
        # They are used to generate the correct cache key
        data = cache.get(Document.cache_key(**kwargs), {})
        data[message.user.pk] = message.user.get_full_name()
        cache.set(Document.cache_key(**kwargs), data)
        # update of the clients connected to the list is handled in the super
        super(DocumentDetailStatusConsumer, self).connect(message, **kwargs)
        self.notify_current_document()

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        data = cache.get(Document.cache_key(**kwargs), {})
        data.pop(message.user.pk, None)
        cache.set(Document.cache_key(**kwargs), data)
        self.notify_current_document()
        self.notify_documents()
        super(DocumentDetailStatusConsumer, self).disconnect(message, **kwargs)


class Demultiplexer(WebsocketDemultiplexer):
    """
    This multiplexed implementation send notification whenever a document is updated

    It uses data binding to listen for changes to the attached model and send a message
    with the document updates.
    By using multiplexing we can easily add different consumers and reduce the frontend code.
    """
    consumers = {
        'document': DocumentBinding.consumer,
    }

    def connection_groups(self):
        return ['notifications']

# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer  # , WebsocketDemultiplexer
from django.core.cache import cache

from .models import Document


class UserCounterConsumer(JsonWebsocketConsumer):
    """
    This consumer is responsible for registering all the currently active users
    to send them generic notifications

    WebsocketConsumer provides a higher level of abstraction by exposing
    `connect`, `disconnect`, `receive` which handles message encoding / decoding.

    We don't need to handle incoming messages, thus the `received` method is not
    implemented.
    """
    # local shortcut
    users_group = 'users'

    groups = (users_group,)
    """
    This consumer will be attached to the general users group

    We want to send messages regarding the documents changes and
    the number of connected users at different times, thus we use
    different groups for the different purposes (consumers)
    """

    def _notify_user_counter(self):
        """
        Counts the users in cache and send the message to the whole group::

            {
                'users': '<number-of-users>'
            }
        """
        msg = {
            'type': 'users.count',
            'message': {
                self.users_group: len(cache.get(f'documents-{self.users_group}', {})),
            }
        }
        async_to_sync(self.channel_layer.group_send)(self.users_group, msg)

    def users_count(self, event):
        """
        Sends back to the connected client

        :param event: payload originated from :py:meth:`_notify_user_counter`
        """
        self.send_json(content=event['message'])

    def connect(self):
        """
        On connect, we count the user as online and we send back the number
        of users currently online.

        Users are counted by saving keeping id/username in a cache dictionary.
        """
        super(UserCounterConsumer, self).connect()
        if self.scope['user'].is_authenticated:
            # let's ignore possible race conditions here :)
            data = cache.get(f'documents-{self.users_group}', {})
            data[self.scope['user'].pk] = self.scope['user'].get_full_name()
            cache.set(f'documents-{self.users_group}', data)
        self._notify_user_counter()

    def disconnect(self, close_code):
        """
        On disconnect, the user is removed
        """
        if self.scope['user'].is_authenticated:
            data = cache.get(f'documents-{self.users_group}', {})
            data.pop(self.scope['user'].pk, None)
            cache.set(f'documents-{self.users_group}', data)
        self._notify_user_counter()
        super(UserCounterConsumer, self).disconnect(close_code)


class DocumentListConsumer(JsonWebsocketConsumer):
    """
    This provides the status of each document with the list of attached users and their phases

    When a client connects, an update is sent to all the connected clients to inform them
    about the document statuses
    """

    #: we track two document states: read, update
    phases = [Document.Status.read, Document.Status.update]

    @property
    def groups(self):
        """
        Attached do the documents list group
        """
        return Document.Status.list,

    def notify_documents(self):
        """
        Send the list of users in each phase of each document to all the consumers in the
        ``Document.Status.list`` channel via a ``document_status`` event,
         handled by :py:meth:`document_status` method
        """
        async_to_sync(self.channel_layer.group_send)(Document.Status.list, {
            'type': 'document.status',
            'message': self.get_status_packet()
        })

    def get_status_packet(self):
        """
        The list of users in each phase of each document is packed in a message
        """
        statuses = {}
        for document in Document.objects.all().values_list('slug', flat=True):
            statuses[document] = {
                phase: cache.get(Document.cache_key(document, phase), {}) for phase in self.phases
            }
            statuses[document]['document'] = document
        return statuses

    def document_status(self, event):
        """
        Sends back to the connected client

        :param event: payload originated from :py:meth:`notify_documents` or :py:meth:`notify_current_document`
        """
        self.send_json(content=event['message'])

    def connect(self):
        """
        Send the the status of all the documents (i.e: the list of connected users for each document/phase) to the
        generic group
        """
        super(DocumentListConsumer, self).connect()
        self.notify_documents()


class DocumentDetailConsumer(DocumentListConsumer):
    """
    This consumer tracks the status of the different documents.

    When a user connect/disconnect, a frame is sent to all the clients, both the ones connected to the specific
    document, and the ones on the list of documents

    Is attached to a route without a slug, it will reports the status of all the documents
    """

    @property
    def slug(self):
        """
        slug is part of the routing path and is available in the scope

        This is a convenience property for more readable code

        :return: string
        """
        return self.scope['url_route']['kwargs'].get('slug')

    @property
    def groups(self):
        """
        If consumer is attached to a document, is registered on the document-specific group
        """
        return [self.slug, Document.Status.list]

    def notify_current_document(self):
        """
        Send the current document status to all the consumers in the
        ``Document.Status.list`` channel via a ``document_status`` event,
         handled by :py:meth:`document_status` method
        """
        async_to_sync(self.channel_layer.group_send)(self.slug, {
            'type': 'document.status',
            'message': self.get_status_packet()
        })

    def get_status_packet(self):
        """
        The numbers of users in each of the current document phases is packed
        """
        statuses = {
            phase: cache.get(Document.cache_key(self.slug, phase), {}) for phase in self.phases
        }
        statuses['document'] = self.slug
        return statuses

    def _update_document_count(self, user_string=None):
        """
        Update the document counting structure. If user_string is empty, current user is remove, otherwise is
        added to the list of users on the current document

        :param user_string: user full name (or None if user is disonnecting)
        """
        # self.scope['url_route'] contains the routing matching parameters
        # {'slug': <document-slug>, 'phase': 'read|update'}
        # They are used to generate the correct cache key
        data = cache.get(Document.cache_key(**self.scope['url_route']['kwargs']), {})
        if user_string:
            data[self.scope['user'].pk] = user_string
        else:
            data.pop(self.scope['user'].pk, None)
        cache.set(Document.cache_key(**self.scope['url_route']['kwargs']), data)

    def connect(self):
        """
        When opening the detail / form, the current user is assigned to the correct phase, then
        the users connected to the list received all the documents statuses while the ones connected
        to the current document are updated about it
        """
        self._update_document_count(self.scope['user'].get_full_name())
        # update of the clients connected to the list is handled in the super
        super(DocumentDetailConsumer, self).connect()
        self.notify_current_document()

    def disconnect(self, code):
        """
        Do some cleanup on connection close:

        * Remove user from document
        * Notify users on the document and documents list
        """
        self._update_document_count(None)
        self.notify_current_document()
        self.notify_documents()
        super(DocumentDetailConsumer, self).disconnect(code)

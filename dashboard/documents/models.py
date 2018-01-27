# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.db.models import ImageField
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


@python_2_unicode_compatible
class Document(TimeStampedModel):
    class Status(object):
        read = 'read'
        update = 'update'
        list = 'documents'

    title = models.CharField(_('title'), max_length=767)
    slug = models.SlugField(_('slug'), max_length=767, unique=True)
    image = ImageField(_('image'), null=True)
    abstract = RichTextField(_('abstract'), null=True)
    text = RichTextField(_('content'), null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'), null=True)

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('document-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Document, self).save(*args, **kwargs)

    @staticmethod
    def group(slug, phase):
        return f'documents-{slug}-{phase}'

    @staticmethod
    def cache_key(slug, phase, **kwargs):
        return f'documents-{slug}-{phase}'

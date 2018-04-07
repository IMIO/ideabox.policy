# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from datetime import datetime
from hashlib import md5
from operator import attrgetter
from plone import api
from random import shuffle


class ProjectsView(BrowserView):

    _keys = {
        0: 'UID',
        1: 'Title',
        2: 'created',
        3: 'modified',
    }

    @property
    def random_sort_key(self):
        key = ord(self.random_key[:1])
        return self._keys[key % len(self._keys)]

    def random_sort(self, elements):
        elements._sequence = sorted(
            elements._sequence,
            key=attrgetter(self.random_sort_key),
        )
        return elements

    def sort_items(self, elements):
        elements = [e for e in elements]
        shuffle(elements)
        return elements

    @property
    def random_key(self):
        now = datetime.now()
        return md5(u'{0}-{1}'.format(
            self.request.get('HTTP_USER_AGENT', now.strftime('%m%Y')),
            now.strftime('%d'),
        )).hexdigest()

    @property
    def default_image(self):
        return '{0}/project_default.jpg'.format(
            api.portal.get().absolute_url(),
        )

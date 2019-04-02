# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from datetime import datetime
from hashlib import md5
from ideabox.policy.utils import can_view_rating
from operator import attrgetter
from plone import api
from random import shuffle
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class ProjectsView(BrowserView):

    _keys = {0: "UID", 1: "Title", 2: "created", 3: "modified"}

    @property
    def random_sort_key(self):
        key = ord(self.random_key[:1])
        return self._keys[key % len(self._keys)]

    def random_sort(self, elements):
        elements = sorted(
            elements, key=attrgetter(self.random_sort_key)
        )
        return elements

    def sort_items(self, elements):
        elements = [e for e in elements]
        shuffle(elements)
        return elements

    @property
    def random_key(self):
        now = datetime.now()
        return md5(
            u"{0}-{1}".format(
                self.request.get("HTTP_USER_AGENT", now.strftime("%m%Y")),
                now.strftime("%d"),
            )
        ).hexdigest()

    @property
    def default_image(self):
        return "{0}/project_default.jpg".format(api.portal.get().absolute_url())

    def rating(self, context):
        return can_view_rating(context)

    def get_theme(self, key):
        if not hasattr(self, "_themes"):
            factory = getUtility(IVocabularyFactory, "collective.taxonomy.theme")
            self._themes = factory(self.context)
        try:
            return self._themes.getTerm(key).title
        except KeyError:
            return ""

# -*- coding: utf-8 -*-

from datetime import datetime
from eea.facetednavigation.interfaces import IFacetedLayout
from hashlib import md5


def faceted_query_handler(obj, event):
    if obj.REQUEST.ACTUAL_URL.endswith("@@faceted_query"):
        try:
            layout = IFacetedLayout(obj).layout
        except TypeError:
            layout = None
        if layout == "faceted-project":
            event.query["sort_on"] = Randomizer(obj.REQUEST).random_sort_key
            event.query["sort_order"] = "ascending"


class Randomizer(object):

    _keys = {0: "UID", 1: "sortable_title", 2: "created", 3: "modified"}

    def __init__(self, request):
        self.request = request

    @property
    def random_sort_key(self):
        key = ord(self.random_key[:1])
        return self._keys[key % len(self._keys)]

    @property
    def random_key(self):
        now = datetime.now()
        return md5(
            u"{0}-{1}".format(
                self.request.get("HTTP_USER_AGENT", now.strftime("%m%Y")),
                now.strftime("%d"),
            )
        ).hexdigest()

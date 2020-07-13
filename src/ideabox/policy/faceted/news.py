# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from ideabox.policy import utils


class NewsView(BrowserView):

    def format_date(self, value):
        return utils.localized_month(value.strftime("%d %B %Y"), self.request)

# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from plone import api

from ideabox.policy import _


class SummaryView(BrowserView):

    def get_summary(self):
        return (
            {
                'state': 'study_in_progress',
                'count': self.count('study_in_progress'),
                'description': _(u'diagnose and analysis'),
            },
            {
                'state': 'in_progress',
                'count': self.count('in_progress'),
                'description': _(u'Setting up'),
            },
            {
                'state': 'realized',
                'count': self.count('realized'),
                'description': None,
            },
        )

    def count(self, state):
        return len(api.content.find(
            context=self.context,
            portal_type='Project',
            review_state=state,
        ))

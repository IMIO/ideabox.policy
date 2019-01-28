# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase
from zope.component import getMultiAdapter


class UserMenuViewlet(ViewletBase):

    index = ViewPageTemplateFile('templates/user_menu.pt')

    def user_actions(self):
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')

        actions = context_state.actions('user_menu')
        return actions

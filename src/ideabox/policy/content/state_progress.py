# -*- coding: utf-8 -*-
from ideabox.policy import _
from plone.app.textfield import RichText
from plone.dexterity.browser import view
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IStateProgress(model.Schema):
    """IStateProgress"""

    state_date = schema.Date(title=_(u"Date"), required=True)

    body = RichText(title=_(u"Content"), required=True)


@implementer(IStateProgress)
class StateProgress(Container):
    pass


class StateProgressView(view.DefaultView):
    pass

# -*- coding: utf-8 -*-

from ideabox.policy import _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class ICampaign(model.Schema):
    project_submission = schema.Bool(
        title=_(u"Enable / Disable project submission"), default=False,
    )


@implementer(ICampaign)
class Campaign(Container):
    pass

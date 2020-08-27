# encoding: utf-8

from hashlib import md5
from ideabox.policy import _
from ideabox.policy.faceted.subscriber import Randomizer
from ideabox.policy.utils import can_view_rating
from plone import api
from plone.supermodel.model import Schema
from plone.tiles import Tile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from random import shuffle
from zope import schema
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class INewsletterTile(Schema):
    """A tile that displays a listing of content items"""

    title = schema.TextLine(title=_(u"Title"), required=True, default=_(u"Newsletter"))

    newsletter_link = schema.TextLine(
        title=_(u"Newsletter link"),
        required=True,
    )


class NewsletterTile(Tile):
    template = ViewPageTemplateFile("templates/newsletter.pt")

    def __call__(self):
        return self.template()

    @property
    def title(self):
        return self.data.get("title") or _(u"Newsletter")

    @property
    def newsletter_link(self):
        return self.data.get("newsletter_link")

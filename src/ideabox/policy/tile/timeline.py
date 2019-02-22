# encoding: utf-8
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.supermodel.model import Schema
from plone.tiles import Tile


class ITimelineTile(Schema):
    """A tile that displays a listing of content items"""


class TimelineTile(Tile):
    """A tile that displays a listing of content items"""

    template = ViewPageTemplateFile('templates/timeline.pt')

    def __call__(self):
        return self.template()

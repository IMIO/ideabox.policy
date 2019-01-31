# encoding: utf-8
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.standardtiles import PloneMessageFactory as _
from plone.supermodel.model import Schema
from plone.tiles import Tile
from zope import schema


class IProjectsTile(Schema):
    """A tile that displays a listing of content items"""

    limit = schema.Int(
        title=_(u'Limit'),
        description=_(u'Limit projects'),
        required=False,
        default=100,
        min=1,
    )


class ProjectsTile(Tile):
    """A tile that displays a listing of content items"""

    template = ViewPageTemplateFile('templates/tile_projects.pt')

    def __call__(self):
        return self.template()

    def contents(self):
        return ''

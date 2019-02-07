# encoding: utf-8
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.standardtiles import PloneMessageFactory as _
from plone.supermodel.model import Schema
from plone.tiles import Tile
from zope import schema
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class IProjectsTile(Schema):
    """A tile that displays a listing of content items"""

    limit = schema.Int(
        title=_(u'Limit'),
        description=_(u'Limit projects'),
        required=False,
        default=10,
        min=1,
    )


class ProjectsTile(Tile):
    """A tile that displays a listing of content items"""

    template = ViewPageTemplateFile('templates/tile_projects.pt')

    def __call__(self):
        return self.template()

    def contents(self):
        limit = self.data["limit"]
        catalog = api.portal.get_tool('portal_catalog')
        results = catalog.searchResults(
            portal_type='Project',
            sort_on='created',
            sort_order='reverse',
        )[:limit]
        return results

    def get_images(self, project):
        results = project.getObject().listFolderContents(contentFilter={"portal_type": "Image"})
        if results:
            return results[0]
        return None

    def get_theme(self, project):
        results = []
        registry = getUtility(IRegistry)
        dict_value = registry.get('ideabox.vocabulary.theme')
        for theme in project.project_theme:
            results.append(dict_value[theme])
        return results

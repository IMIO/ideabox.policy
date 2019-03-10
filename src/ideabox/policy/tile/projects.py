# encoding: utf-8

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ideabox.policy import _
from ideabox.policy.utils import can_view_rating
from plone import api
from plone.supermodel.model import Schema
from plone.tiles import Tile
from zope import schema
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class IProjectsTile(Schema):
    """A tile that displays a listing of content items"""

    limit = schema.Int(
        title=_(u"Limit"),
        description=_(u"Limit projects"),
        required=False,
        default=10,
        min=1,
    )


class ProjectsTile(Tile):
    """A tile that displays a listing of content items"""

    template = ViewPageTemplateFile("templates/projects.pt")

    def __call__(self):
        return self.template()

    def contents(self):
        limit = self.data["limit"]
        return api.content.find(
            portal_type="Project", sort_on="created", sort_order="reverse"
        )[:limit]

    def get_theme(self, key):
        if not hasattr(self, "_themes"):
            factory = getUtility(IVocabularyFactory, "collective.taxonomy.theme")
            self._themes = factory(self.context)
        try:
            return self._themes.getTerm(key).title
        except KeyError:
            return ""

    @property
    def default_image(self):
        return "{0}/project_default.jpg".format(api.portal.get().absolute_url())

    def rating(self, context):
        return can_view_rating(context)

# -*- coding: utf-8 -*-
"""
ideabox.policy
--------------
 Affinitic SPRL

"""
from zope import schema

from ideabox.policy import _
from ideabox.policy import vocabularies
from plone.app.textfield import RichText
from plone.dexterity.browser import view
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implements


class IProject(model.Schema):
    """IProject"""

    project_type = schema.Choice(
        title=_(u"Type"),
        source=vocabularies.types,
        required=True
    )

    body = RichText(
        title=u"Contenu",
        required=True,
    )


class Project(Container):
    implements(IProject)


class ProjectView(view.DefaultView):

    @property
    def get_images_url(self):
        contents = self.context.listFolderContents(contentFilter={"portal_type": "Image"})
        images_url = []
        for content in contents:
            images_url.append(content.absolute_url)
        return images_url

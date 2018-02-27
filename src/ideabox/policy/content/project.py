# -*- coding: utf-8 -*-
"""
ideabox.policy
--------------
 Affinitic SPRL

"""
from zope import schema

from collective.z3cform.select2.widget.widget import MultiSelect2FieldWidget
from plone.app.textfield import RichText
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implements
from plone.dexterity.browser import view

from ideabox.policy import _
from ideabox.policy import vocabularies


class IProject(model.Schema):
    """IProject"""

    project_type = schema.Choice(
        title=_(u"Type"),
        source=vocabularies.types,
        required=True
    )

    form.widget(category=MultiSelect2FieldWidget)
    category = schema.List(
        title=_(u'Categories'),
        value_type=schema.Choice(
            title=_(u'Categories'),
            source=vocabularies.categories,
        ),
        required=False,
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

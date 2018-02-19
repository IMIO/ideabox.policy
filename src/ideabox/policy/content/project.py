# -*- coding: utf-8 -*-
"""
ideabox.policy
--------------
 Affinitic SPRL

"""
from collective.z3cform.select2.widget.widget import MultiSelect2FieldWidget
from plone.autoform import directives as form
from zope.interface import Interface, implements
from zope import schema
from ideabox.policy import _
from plone.supermodel import model
from plone.dexterity.content import Container
from ideabox.policy import vocabularies


class IProject(model.Schema):
    """IProject"""

    projecttype = schema.Choice(
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



class Project(Container):
    implements(IProject)

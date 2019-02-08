# -*- coding: utf-8 -*-

from plone.supermodel import model
from plone import schema
from plone.app.users.browser.userdatapanel import UserDataPanel
from plone.z3cform.fieldsets import extensible
from z3c.form import field
from z3c.form.browser.radio import RadioFieldWidget
from zope.component import adapts
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from ideabox.policy import _


class IEnhancedUserDataSchema(model.Schema):

    last_name = schema.TextLine(
        title=_(u'Last name'),
        required=False
    )

    first_name = schema.TextLine(
        title=_(u'First name'),
        required=False
    )

    gender = schema.Choice(
        title=_(u"Gender"),
        required=False,
        vocabulary=u'ideabox.vocabularies.gender'
    )

    birthdate = schema.Date(
        title=_(u"Birthdate"),
        required=False,
    )

    zip_code = schema.Choice(
        title=_(u'Zip code'),
        required=False,
        vocabulary=u'ideabox.vocabularies.zip_code'
    )


class UserDataPanelExtender(extensible.FormExtender):
    adapts(Interface, IDefaultBrowserLayer, UserDataPanel)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        fields = fields.omit('accept')
        fields['gender'].widgetFactory = RadioFieldWidget
        self.add(fields)
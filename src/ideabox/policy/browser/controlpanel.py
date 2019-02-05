# -*- coding: utf-8 -*-
import re

from plone.app.registry.browser import controlpanel
from ideabox.policy import _
from zope import schema
from zope.interface import Interface
from Products.validation.validators.BaseValidators import EMAIL_RE


class InvalidEmailError(schema.ValidationError):
    __doc__ = u'Please enter a valid e-mail address.'


def isEmail(value):
    if re.match('^'+EMAIL_RE, value):
        return True
    raise InvalidEmailError


class IIdeaBoxSettingsSchema(Interface):

    project_manger_email = schema.TextLine(
        title=_(u'Email address of the project manager'),
        constraint=isEmail
    )


class IdeaBoxSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IIdeaBoxSettingsSchema
    label = _(u'Email address of the project manager')
    description = _(u'')

    def updateFields(self):
        super(IdeaBoxSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(IdeaBoxSettingsEditForm, self).updateWidgets()


class IdeaBoxSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = IdeaBoxSettingsEditForm

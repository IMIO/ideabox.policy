# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from ideabox.policy import _
from zope import schema
from zope.interface import Interface


class InvalidEmailError(schema.ValidationError):
    __doc__ = u'Please enter a valid e-mail address.'


class IIdeaBoxSettingsSchema(Interface):

    project_manger_email = schema.TextLine(
        title=_(u'Email address of the project manager'),
        description=_(u'If there are multiple email addresses, separate them with semicolons'),  # noqa
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

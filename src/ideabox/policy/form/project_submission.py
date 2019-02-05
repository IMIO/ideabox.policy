# -*- coding: utf-8 -*-
import z3c.form
import zope.interface

from collective.z3cform.select2.widget.widget import MultiSelect2FieldWidget
from ideabox.policy import _
from ideabox.policy.content.project import IProject
from ideabox.policy.utils import execute_under_admin
from plone import api
from plone.namedfile.field import NamedBlobImage
from plone.registry.interfaces import IRegistry
from z3c.form import button
from z3c.form.interfaces import HIDDEN_MODE
from zope import schema
from zope.component import getUtility
from zope.i18n import translate


class IProjectSubmission(IProject):
    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    project_image = NamedBlobImage(
        title=_(u'Project image'),
        required=False,
    )


class ProjectSubmissionForm(z3c.form.form.Form):

    zope.interface.implements(z3c.form.interfaces.IFieldsForm)
    fields = z3c.form.field.Fields(IProjectSubmission).select(
        'title',
        'project_theme',
        'project_district',
        'body',
        'project_image',
        'original_author',
    )
    fields['project_theme'].widgetFactory = MultiSelect2FieldWidget
    fields['project_district'].widgetFactory = MultiSelect2FieldWidget

    fields['original_author'].mode = HIDDEN_MODE

    ignoreContext = True

    def update(self):
        super(ProjectSubmissionForm, self).update()
        self.widgets['original_author'].value = \
            api.user.get_current().getProperty('fullname')

    def send_mail(self, data):
        lang = api.portal.get_current_language()[:2]
        rec_email = api.portal.get_registry_record(
            'ideabox.policy.browser.controlpanel.IIdeaBoxSettingsSchema.project_manger_email'  # noqa
        )
        # TODO
        # body = translate(
        #     _(u"email_body_project_submission",
        #       default=u"""""",
        #       mapping={}
        #       ),
        #     target_language=lang,
        # )
        # api.portal.send_email(
        #     recipient=rec_email,
        #     subject=translate(
        #         _(u"New project submission"),
        #         target_language=lang,
        #     ),
        #     body=body,
        # )

    def send_request(self, data):
        registry = getUtility(IRegistry)
        portal_url = api.portal.get().absolute_url_path()
        folder = registry.get('ideabox.new.project.folder')
        container = api.content.get(path="{0}/{1}".format(portal_url, folder))

        project_obj = execute_under_admin(
            container,
            api.content.create,
            type='Project',
            title=data['title'],
            project_theme=data['project_theme'],
            body=data['body'].output,
            container=container,
            original_author=data['original_author'])
        api.content.transition(obj=project_obj, transition='deposit')
        if data['project_image']:
            execute_under_admin(
                project_obj,
                api.content.create,
                type='Image',
                title=data['project_image'].filename,
                image=data['project_image'],
                container=project_obj
            )
        self.request.response.redirect(
            "{0}/{1}/{2}".format(portal_url, folder, project_obj.id))

        self.send_mail(data)

    @button.buttonAndHandler(_(u'Send'), name='send')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.send_request(data)

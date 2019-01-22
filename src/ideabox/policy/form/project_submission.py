# encoding: utf-8
import z3c.form
import zope.interface

from ideabox.policy import _
from ideabox.policy.content.project import IProject
from ideabox.policy.utils import execute_under_admin
from plone import api
from plone.namedfile.field import NamedBlobImage
from z3c.form import button
from z3c.form.interfaces import HIDDEN_MODE
from zope import schema


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
        'body',
        'project_image',
        'original_author',
    )

    fields['original_author'].mode = HIDDEN_MODE

    ignoreContext = True

    def update(self):
        super(ProjectSubmissionForm, self).update()
        self.widgets['original_author'].value = \
            api.user.get_current().getProperty('fullname')

    def send_request(self, data):
        container = api.portal.get().projets

        project_obj = execute_under_admin(
            container,
            api.content.create,
            type='Project',
            title=data['title'],
            project_theme=data['project_theme'],
            body=data['body'].output,
            container=container,
            original_author=data['original_author'])
        if data['project_image']:
            execute_under_admin(
                project_obj,
                api.content.create,
                type='Image',
                title=data['project_image'].filename,
                image=data['project_image'],
                container=project_obj
            )

    @button.buttonAndHandler(_(u'Send'), name='send')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.send_request(data)

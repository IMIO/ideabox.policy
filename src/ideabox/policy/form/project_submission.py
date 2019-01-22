# encoding: utf-8
import z3c.form
import zope.interface

from ideabox.policy import _
from ideabox.policy.content.project import IProject
from plone.namedfile.field import NamedBlobImage
from z3c.form import button
from z3c.form.interfaces import HIDDEN_MODE


class IProjectSubmission(IProject):

    project_image = NamedBlobImage(
        title=_(u'Project image'),
        required=False,
    )


class ProjectSubmissionForm(z3c.form.form.Form):

    zope.interface.implements(z3c.form.interfaces.IFieldsForm)
    fields = z3c.form.field.Fields(IProjectSubmission)

    fields['original_author'].mode = HIDDEN_MODE

    ignoreContext = True

    def send_request(self):
        """TO DO"""

    @button.buttonAndHandler(_(u'Send'), name='send')
    def handleApply(self, action):
        self.send_request()

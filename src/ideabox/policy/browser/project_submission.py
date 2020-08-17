# -*- coding: utf-8 -*-

from ideabox.policy.form.project_submission import ProjectSubmissionForm
from plone.z3cform.layout import FormWrapper


class ProjectSubmissionView(FormWrapper):
    form = ProjectSubmissionForm

    def enable_submission(self):
        context = self.context
        return context.project_submission

# -*- coding: utf-8 -*-

from plone.z3cform.layout import FormWrapper
from ideabox.policy.form.project_submission import ProjectSubmissionForm


class ProjectSubmissionView(FormWrapper):
    form = ProjectSubmissionForm

# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from plone.app.textfield import RichText
from plone.dexterity.browser import view
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implements

from ideabox.policy import _
from ideabox.policy import vocabularies


class IProject(model.Schema):
    """IProject"""

    project_type = schema.Choice(
        title=_(u"Type"),
        source=vocabularies.types,
        required=True
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

    def get_project_status(self):
        history = self.get_history_project()
        return history[0].get('review_state')

    def get_history_project(self):
        history = self.context.workflow_history.values()[0]
        history = list(history)
        history.reverse()
        return history

    def generate_draft_time_line(self, state, history):
        draft_date = ''
        deposited_date = ''
        project_analysis_date = ''
        vote_date = ''
        result_analysis_date = ''
        for status in history:
            if status.get('review_state') == 'result_analysis' \
               and result_analysis_date == '' \
               and state == 'result_analysis':
                result_analysis_date = status.get('time')
            if status.get('review_state') == 'vote' \
               and vote_date == '' \
               and state in ['result_analysis', 'vote']:
                vote_date = status.get('time')
            if status.get('review_state') == 'project_analysis' \
               and project_analysis_date == '' \
               and state in ['result_analysis', 'vote', 'project_analysis']:
                project_analysis_date = status.get('time')
            if status.get('review_state') == 'deposited' \
               and deposited_date == '' \
               and state in ['result_analysis', 'vote', 'project_analysis', 'deposited']:
                deposited_date = status.get('time')
            if status.get('review_state') == 'draft' and draft_date == '':
                draft_date = status.get('time')
        return [draft_date, deposited_date, project_analysis_date, vote_date, result_analysis_date]

    def generate_selected_time_line(self, state, history):
        selected_date = ''
        study_in_progress_date = ''
        in_progress_date = ''
        realized_date = ''
        for status in history:
            if status.get('review_state') == 'realized' \
               and realized_date == '' \
               and state == 'realized':
                realized_date = status.get('time')
            if status.get('review_state') == 'in_progress' \
               and in_progress_date == '' \
               and state in ['realized', 'in_progress']:
                in_progress_date = status.get('time')
            if status.get('review_state') == 'study_in_progress' \
               and study_in_progress_date == '' \
               and state in ['realized', 'in_progress', 'study_in_progress']:
                study_in_progress_date = status.get('time')
            if status.get('review_state') == 'selected' and selected_date == '':
                selected_date = status.get('time')
        return [selected_date, study_in_progress_date, in_progress_date, realized_date]

    def generate_rejected_time_line(self, state, history):
        # Status rejected
        draft_date = ''
        deposited_date = ''
        project_analysis_date = ''
        vote_date = ''
        result_analysis_date = ''
        rejected_date = ''

        for status in history:
            if status.get('review_state') == 'rejected' \
               and rejected_date == '' \
               and state == 'result_analysis':
                rejected_date = status.get('time')
            if status.get('review_state') == 'result_analysis' \
               and result_analysis_date == '' \
               and state in ['rejected', 'result_analysis']:
                result_analysis_date = status.get('time')
            if status.get('review_state') == 'vote' \
               and vote_date == '' \
               and state in ['rejected', 'result_analysis', 'vote']:
                vote_date = status.get('time')
            if status.get('review_state') == 'project_analysis' \
               and project_analysis_date == '' \
               and state in ['rejected', 'result_analysis', 'vote', 'project_analysis']:
                project_analysis_date = status.get('time')
            if status.get('review_state') == 'deposited' \
               and deposited_date == '' \
               and state in ['rejected', 'result_analysis', 'vote', 'project_analysis', 'deposited']:
                deposited_date = status.get('time')
            if status.get('review_state') == 'draft' and draft_date == '':
                draft_date = status.get('time')
        return [draft_date, deposited_date, project_analysis_date, vote_date, result_analysis_date, rejected_date]

    def get_workflow_history(self):
        state = self.get_project_status()
        history = self.get_history_project()
        if state in ['draft', 'deposited', 'project_analysis', 'vote', 'result_analysis']:
            time_line = self.generate_draft_time_line(state, history)
        elif state in ['selected', 'study_in_progress', 'in_progress', 'realized']:
            time_line = self.generate_selected_time_line(state, history)
        else:
            # Status rejected
            time_line = self.generate_rejected_time_line(state, history)

        format_time_line = []
        for date_time in time_line:
            if date_time != '':
                format_time_line.append([date_time.strftime('%d'), date_time.strftime('%b')])
            else:
                format_time_line.append(['', ''])

        return format_time_line

    def get_time_line_title(self):
        state = self.get_project_status()

        if state in ['draft', 'deposited', 'project_analysis', 'vote', 'result_analysis']:
            time_line_title = [_(u'Draft', u'Draft'),
                               _(u'Deposited', u'Deposited'),
                               _(u'Project analysis', u'Project analysis'),
                               _(u'Vote', u'Vote'),
                               _(u'Result analysis', u'Result analysis')
                               ]
        elif state in ['selected', 'study_in_progress', 'in_progress', 'realized']:
            time_line_title = [_(u'Selected', u'Selected'),
                               _(u'Study in progress', u'Study in progress'),
                               _(u'In progress', u'In progress'),
                               _(u'Realized', u'Realized')
                               ]
        else:
            time_line_title = [_(u'Draft', u'Draft'),
                               _(u'Deposited', u'Deposited'),
                               _(u'Project analysis', u'Project analysis'),
                               _(u'Vote', u'Vote'),
                               _(u'Result analysis', u'Result analysis'),
                               _(u'Rejected', u'Rejected')
                               ]
        return time_line_title

    def get_current_status(self):
        state = self.get_project_status()
        states = {
            'draft': _(u'Draft', u'Draft'),
            'deposited': _(u'Deposited', u'Deposited'),
            'project_analysis': _(u'Project analysis', u'Project analysis'),
            'vote': _(u'Vote', u'Vote'),
            'result_analysis': _(u'Result analysis', u'Result analysis'),
            'rejected': _(u'Rejected', u'Rejected'),
            'selected': _(u'Selected', u'Selected'),
            'study_in_progress': _(u'Study in progress', u'Study in progress'),
            'in_progress': _(u'In progress', u'In progress'),
            'realized': _(u'Realized', u'Realized')
        }
        return states.get(state)

    def get_last_step(self):
        state = self.get_project_status()
        states = {
            'draft': 0,
            'deposited': 1,
            'project_analysis': 2,
            'vote': 3,
            'result_analysis': 4,
            'rejected': 5,
            'selected': 0,
            'study_in_progress': 1,
            'in_progress': 2,
            'realized': 0
        }
        return states.get(state)

    def creator(self):
        return self.context.Creator()

    def author(self):
        membership = getToolByName(self.context, 'portal_membership')
        return membership.getMemberInfo(self.creator())

    def authorname(self):
        author = self.author()
        return author and author['fullname'] or self.creator()

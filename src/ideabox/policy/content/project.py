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

    def get_workflow_history(self):
        history = self.context.workflow_history.values()[0]
        history = list(history)
        history.reverse()

        state = history[0].get('review_state')
        if state in ['draft', 'deposited', 'project_analysis', 'vote', 'result_analysis']:
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
                time_line = [draft_date, deposited_date, project_analysis_date, vote_date, result_analysis_date]
        elif state in ['selected', 'study_in_progress', 'in_progress', 'realized']:
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
                time_line = [selected_date, study_in_progress_date, in_progress_date, realized_date]
        else:
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
                time_line = [draft_date, deposited_date, project_analysis_date, vote_date, result_analysis_date, rejected_date]

        format_time_line = []
        for date_time in time_line:
            if date_time != '':
                format_time_line.append([date_time.strftime('%d'), date_time.strftime('%b')])

            else:
                format_time_line.append(['', ''])

        return format_time_line

    def get_time_line_title(self):
        history = self.context.workflow_history.values()[0]
        history = list(history)
        history.reverse()
        state = history[0].get('review_state')

        if state in ['draft', 'deposited', 'project_analysis', 'vote', 'result_analysis']:
            time_line_title = [_(u'draft'),
                               _(u'deposited'),
                               _(u'project analysis'),
                               _(u'vote'),
                               _(u'result analysis')
                               ]
        elif state in ['selected', 'study_in_progress', 'in_progress', 'realized']:
            time_line_title = [_(u'selected'),
                               _(u'study in progress'),
                               _(u'in progress'),
                               _(u'realized')
                               ]
        else:
            time_line_title = [_(u'draft'),
                               _(u'deposited'),
                               _(u'project analysis'),
                               _(u'vote'),
                               _(u'result analysis'),
                               _(u'rejected')
                               ]
        return time_line_title

    def get_current_status(self):
        history = self.context.workflow_history.values()[0]
        history = list(history)
        history.reverse()

        state = history[0].get('review_state')
        if state == 'draft':
            state = _(u'draft')
        if state == 'deposited':
            state = _(u'deposited')
        if state == 'project_analysis':
            state = _(u'project analysis')
        if state == 'vote':
            state = _(u'vote')
        if state == 'result_analysis':
            state = _(u'result analysis')
        if state == 'rejected':
            state = _(u'rejected')
        if state == 'selected':
            state = _(u'selected')
        if state == 'study_in_progress':
            state = _(u'study in progress')
        if state == 'in_progress':
            state = _(u'in progress')
        if state == 'realized':
            state = _(u'realized')

        return state

    def creator(self):
        return self.context.Creator()

    def author(self):
        membership = getToolByName(self.context, 'portal_membership')
        return membership.getMemberInfo(self.creator())

    def authorname(self):
        author = self.author()
        return author and author['fullname'] or self.creator()

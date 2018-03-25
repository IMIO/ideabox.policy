# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from plone import api
from plone.app.textfield import RichText
from plone.dexterity.browser import view
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implements

from ideabox.policy import _


class IProject(model.Schema):
    """IProject"""

    project_theme = schema.Choice(
        title=_(u"Theme"),
        vocabulary=u'ideabox.vocabularies.theme',
        required=True
    )

    body = RichText(
        title=u"Contenu",
        required=True,
    )


class Project(Container):
    implements(IProject)


class ProjectView(view.DefaultView):

    _timeline_states = (
        'deposited',
        'project_analysis',
        'vote',
        'result_analysis',
        'study_in_progress',
        'in_progress',
        'realized',
    )

    @property
    def get_images_url(self):
        contents = self.context.listFolderContents(contentFilter={"portal_type": "Image"})
        images_url = []
        for content in contents:
            images_url.append(content.absolute_url())
        return images_url

    def get_news(self):
        return reversed(api.content.find(
            context=self.context,
            portal_type='News Item',
            sort_on='Date',
        ))

    @property
    def review_state(self):
        return api.content.get_state(obj=self.context)

    @property
    def before_selected(self):
        return self.review_state in self._timeline_states[:4] + ('rejected', )

    @property
    def _workflow_history(self):
        history = [
            {
                'order': self._timeline_states.index(l.get('review_state')),
                'state': l.get('review_state'),
                'date': l.get('time'),
            }
            for l in self.context.workflow_history.values()[0]
            if l.get('review_state') in self._timeline_states
        ]
        return sorted(history, key=lambda x: x['order'])

    @property
    def can_view_timeline(self):
        if self.review_state is 'rejected':
            return False
        return self.review_state in self._timeline_states

    @property
    def timeline_states(self):
        history = self._workflow_history
        current_state = self.review_state
        first_timeline_states = self._timeline_states[:4]
        second_timeline_states = self._timeline_states[4:]
        selected_states = (self.review_state in first_timeline_states and
                           first_timeline_states or second_timeline_states)
        states = [{'state': e, 'date': '', 'class': u'unfinished'}
                  for e in selected_states]
        idx = current_state in self._timeline_states \
            and self._timeline_states.index(current_state) or 0
        for line in history:
            # Ensure that next steps that were completed in the past is not
            # displayed
            if line['order'] > idx:
                break
            state = [s for s in states if s['state'] == line['state']]
            if len(state) == 1:
                state[0]['date'] = line['date']
                state[0]['class'] = u'finished'
        return states

    @property
    def anonymous(self):
        return api.user.is_anonymous()

    def creator(self):
        return getattr(self.context, 'original_author', self.context.Creator())

    def author(self):
        membership = getToolByName(self.context, 'portal_membership')
        return membership.getMemberInfo(self.creator())

    def authorname(self):
        author = self.author()
        return author and author['fullname'] or self.creator()

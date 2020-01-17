# -*- coding: utf-8 -*-

from plone import api
from plone.registry import Record
from plone.registry import field
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def add_legal_informations_in_registry_1002(context):
    registry = getUtility(IRegistry)
    registry_field = field.TextLine(title=u"Legal informations")
    key = "ideabox.policy.browser.controlpanel.IIdeaBoxSettingsSchema.legal_informations"
    registry_record = Record(registry_field)
    # registry_record.value = u""
    if key not in registry:
        registry.records[key] = registry_record

def fix_comments_1001(context):
    from plone.app.discussion.interfaces import IConversation

    brains = api.content.find(
        context=api.portal.get(),
        total_comments={"query": [1, 1000], "range": "min:max"},
    )
    for brain in brains:
        obj = brain.getObject()
        conversation = IConversation(obj, None)
        for thread in conversation.getThreads():
            comment = thread["comment"]
            if comment.author_name == comment.author_email:
                user = api.user.get(username=comment.author_username)
                infos = [user.getProperty("first_name"), user.getProperty("last_name")]
                comment.author_name = " ".join([i for i in infos if i])

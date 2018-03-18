# encoding: utf-8

from zope.i18n import translate

from ideabox.policy import vocabularies


def token_type_recovery(value):
    value = value.decode('utf8')
    vocabulary = vocabularies.ThemeVocabulary(None)
    return [e.token for e in vocabulary.by_value.values()
            if translate(e.title) == value][0]

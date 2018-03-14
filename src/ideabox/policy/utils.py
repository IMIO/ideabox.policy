# encoding: utf-8

from ideabox.policy import vocabularies


def token_type_recovery(value):
    value = value.decode('utf8')
    return [e.token for e in vocabularies.types(None).by_value.values()
            if e.title == value][0]

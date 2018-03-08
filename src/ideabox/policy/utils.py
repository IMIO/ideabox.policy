# encoding: utf-8
"""
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""
from ideabox.policy import vocabularies


def token_type_recovery(value):
    value = value.decode('utf8')
    return[e.token for e in vocabularies.types(None).by_value.values() if e.title == value][0]

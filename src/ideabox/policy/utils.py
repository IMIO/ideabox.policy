# encoding: utf-8
"""
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""
from ideabox.policy import vocabularies


def token_type_recorevery(value):
    value = value.decode('utf8')
    return[e.token for e in vocabularies.types(None).by_value.values() if e.title == value][0]


def token_category_recorvery(list_cat):
    list_token = []
    for cat in list_cat:
        value = [e.token for e in vocabularies.categories(None).by_value.values() if e.title == cat.strip()][0]
        list_token.append(value)
    return list_token

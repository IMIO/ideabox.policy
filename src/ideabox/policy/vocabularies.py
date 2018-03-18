# encoding: utf-8

from zope.schema.vocabulary import SimpleVocabulary

from ideabox.policy import _


def dict_list_2_vocabulary(dict_list):
    """dict_list_2_vocabulary
    Converts a dictionary list to a SimpleVocabulary

    :param dict_list: dictionary list
    """
    terms = []
    for item in dict_list:
        for key in sorted([k for k in item]):
            terms.append(SimpleVocabulary.createTerm(
                key, str(key), item[key]))
    return SimpleVocabulary(terms)


class ThemeVocabularyFactory(object):

    def __call__(self, context):
        values = [{'ACPT': _('ACPT', u'Art, Culture, Patrimoine, Tourisme')},
                  {'EVCA': _('EVCA', u'Des espaces verts, des espaces collectifs, des espaces apaisés')},
                  {'IDNA': _('IDNA', u'Idées non attribuées')},
                  {'INCL': _('INCL', u'Inclassables')},
                  {'INSO': _('INSO', u'Inclusion sociale')},
                  {'MOBI': _('MOBI', u'La mobilité')},
                  {'TREN': _('TREN', u'La transition énergétique')},
                  {'VEAU': _('VEAU', u'La végétalisation et l\'agriculture urbaine')},
                  {'VPCN': _('VPCN', u'Ville participative, Collaborative et Numérique')}]
        return dict_list_2_vocabulary(values)


ThemeVocabulary = ThemeVocabularyFactory()

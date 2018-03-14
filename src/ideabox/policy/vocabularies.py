# encoding: utf-8

from zope.interface import alsoProvides
from zope.schema.interfaces import IContextSourceBinder
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


def types(context):
    values = [{'ACPT': _(u'Art, Culture, Patrimoine, Tourisme')},
              {'EVCA': _(u'Des espaces verts, des espaces collectifs, des espaces apaisés')},
              {'IDNA': _(u'Idées non attribuées')},
              {'INCL': _(u'Inclassables')},
              {'INSO': _(u'Inclusion sociale')},
              {'MOBI': _(u'La mobilité')},
              {'TREN': _(u'La transition énergétique')},
              {'VEAU': _(u'La végétalisation et l\'agriculture urbaine')},
              {'VPCN': _(u'Ville participative, Collaborative et Numérique')}]
    return dict_list_2_vocabulary(values)
alsoProvides(types, IContextSourceBinder)


def categories(context):
    values = [{'AGA': _(u'Agriculture et Alimentation')},
              {'AEQ': _(u'Aménager et équiper les quartiers')},
              {'CIT': _(u'Citoyenneté')},
              {'COC': _(u'Collaboratif & Créatif')},
              {'CUL': _(u'Culture')},
              {'DIV': _(u'Divers')},
              {'EMB': _(u'Embellir')},
              {'ERE': _(u'Energie renouvelable et économie d\'énergie')},
              {'ESV': _(u'Espaces verts')},
              {'EVE': _(u'Evénements')},
              {'INC': _(u'Inclusif')},
              {'INF': _(u'Infrastructures')},
              {'MOB': _(u'Mobilité électrique')},
              {'NOE': _(u'Nouveaux équipements')},
              {'NPN': _(u'Nouvelles pratiques et nouveaux services')},
              {'NUM': _(u'Numérique')},
              {'PAR': _(u'Participatif')},
              {'PAT': _(u'Patrimoine')},
              {'PIE': _(u'Piéton')},
              {'POA': _(u'Pollution de l\'air et sonore')},
              {'PRA': _(u'Promotion des arts et des artistes')},
              {'PRD': _(u'Propreté et déchets')},
              {'STA': _(u'Stationnement')},
              {'TOU': _(u'Tourisme')},
              {'TRE': _(u'Transition énergétique')},
              {'TRP': _(u'Transport public')},
              {'VEB': _(u'Végétalisation et Biodiversité')},
              {'VEL': _(u'Vélo')}]
    return dict_list_2_vocabulary(values)
alsoProvides(categories, IContextSourceBinder)

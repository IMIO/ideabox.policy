# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces import INonInstallable
from eea.facetednavigation.layout.layout import FacetedLayout
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility
from zope.interface import implementer

import json
import os


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'ideabox.policy:uninstall',
        ]


def post_install(context):
    """Post install script"""
    portal = api.portal.get()
    if portal.get('projets') is None:
        project = api.content.create(
            type='Folder',
            id='projets',
            title='Projets',
            container=portal,
        )
        api.content.transition(obj=project, transition='publish')
        add_behavior('Folder', 'eea.facetednavigation.subtypes.interfaces.IPossibleFacetedNavigable')
        _activate_dashboard_navigation(project, True, '/faceted/config/projets.xml')
        project_layout = FacetedLayout(project)
        project_layout.update_layout(layout='faceted-project')
    if portal.get('plus-dinfos') is None:
        folder = api.content.create(
            type='Folder',
            id='plus-dinfos',
            title=u"Plus d'infos",
            container=portal,
        )
        api.content.create(
            type='Folder',
            id='edition-2017',
            title=u"Edition 2017",
            container=folder,
        )

    allowed_sizes = api.portal.get_registry_record('plone.allowed_sizes')
    scales = (
        u'banner 1920:610',
        u'project_faceted 450:300',
    )
    for scale in scales:
        if scale not in allowed_sizes:
            allowed_sizes.append(scale)
    api.portal.set_registry_record('plone.allowed_sizes', allowed_sizes)

    api.portal.set_registry_record(
        'collective.behavior.banner.browser.controlpanel.IBannerSettingsSchema.banner_scale',  # noqa
        u'banner'
    )

    menu = {
        '/': [
            {
                'navigation_folder': '/projets',
                'simple_link': '/projets',
                'tab_title': 'Projets',
                'additional_columns': '',
                'condition': 'python: True',
            },
            {
                'navigation_folder': '',
                'simple_link': '/participer',
                'tab_title': 'Participer',
                'additional_columns': '',
                'condition': 'python: True',
            },
            {
                'navigation_folder': '/plus-dinfos',
                'simple_link': '/plus-dinfos',
                'tab_title': "Plus d'infos",
                'additional_columns': '',
                'condition': 'python: True',
            }
        ],
    }
    api.portal.set_registry_record(
        'collective.editablemenu.browser.interfaces.IEditableMenuSettings.menu_tabs_json',  # noqa
        unicode(json.dumps(menu)),
    )


def add_behavior(type_name, behavior_name):
    """Add a behavior to a type"""
    fti = queryUtility(IDexterityFTI, name=type_name)
    if not fti:
        return
    behaviors = list(fti.behaviors)
    if behavior_name not in behaviors:
        behaviors.append(behavior_name)
    fti._updateProperty('behaviors', tuple(behaviors))


def _activate_dashboard_navigation(context, configuration=False, path=None):
    subtyper = context.restrictedTraverse('@@faceted_subtyper')
    if subtyper.is_faceted:
        return
    subtyper.enable()
    if configuration and path:
        context.unrestrictedTraverse('@@faceted_exportimport').import_xml(
            import_file=open(os.path.dirname(__file__) + path)
        )


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.

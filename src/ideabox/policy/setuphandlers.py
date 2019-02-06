# -*- coding: utf-8 -*-
import os

from Products.CMFPlone.interfaces import INonInstallable
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import implementer
from eea.facetednavigation.layout.layout import FacetedLayout


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

    registry = getUtility(IRegistry)
    allowed_sizes = registry.get('plone.allowed_sizes')
    allowed_sizes.append("banner 1920:610")

    api.portal.set_registry_record(
        'collective.behavior.banner.browser.controlpanel.IBannerSettingsSchema.banner_scale',  # noqa
        u'banner'
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

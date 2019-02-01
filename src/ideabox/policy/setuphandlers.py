# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces import INonInstallable
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implementer


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
        api.content.create(
            type='Folder',
            id='projets',
            title='Projets',
            container=portal,
        )
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
    api.portal.set_registry_record(
        'collective.behavior.banner.browser.controlpanel.IBannerSettingsSchema.types',  # noqa
        ['Folder', 'Document']
    )


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.

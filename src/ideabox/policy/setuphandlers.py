# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces import INonInstallable
from plone import api
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


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.

# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'ideabox.policy:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    portal = api.portal.get()
    if portal.get('projects') is None:
            api.content.create(
                type='Folder',
                id='projects',
                title='Projets',
                container=portal
            )


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.

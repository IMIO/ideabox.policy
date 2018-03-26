# -*- coding: utf-8 -*-

from plone.indexer import indexer

from ideabox.policy.content.project import IProject


@indexer(IProject)
def project_picture(obj):
    images = obj.listFolderContents(contentFilter={'portal_type': 'Image'})
    if images:
        obj.image = images[0].image
        return images[0].id

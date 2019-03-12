# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_unicode
from collective.excelexport.exportables.dexterityfields import BaseFieldRenderer
from collective.excelexport.exportables.dexterityfields import (
    DexterityFieldsExportableFactory,
)
from collective.excelexport.exportables.dexterityfields import TextFieldRenderer
from ideabox.policy.export.interfaces import IExtendedProjectExportable
from ideabox.policy.interfaces import IIdeaboxPolicyLayer
from plone import api
from plone.app.textfield.interfaces import IRichText
from z3c.form.interfaces import NO_VALUE
from zope.component import adapts
from zope.component import getAdapters
from zope.interface import Interface
from zope.schema.interfaces import IText
from zope.annotation.interfaces import IAnnotations


class FullTextFieldRenderer(TextFieldRenderer):
    adapts(IText, Interface, IIdeaboxPolicyLayer)

    def render_value(self, obj):
        """Gets the value to render in excel file from content value
        """
        value = self.get_value(obj)
        if not value or value == NO_VALUE:
            return ""

        text = safe_unicode(self._get_text(value))

        return text


class FullRichTextFieldRenderer(FullTextFieldRenderer):
    adapts(IRichText, Interface, IIdeaboxPolicyLayer)

    def _get_text(self, value):
        ptransforms = api.portal.get_tool("portal_transforms")
        return ptransforms.convert("html_to_text", value.output).getData().strip()


class ProjectExportablesFactory(DexterityFieldsExportableFactory):
    portal_types = ["Project"]

    def get_exportables(self):
        project_extended = [
            ad[1] for ad in getAdapters((self.context,), IExtendedProjectExportable)
        ]
        return project_extended


class ExtendedRenderer(BaseFieldRenderer):
    adapts(Interface)
    name = ""

    def __init__(self, context):
        self.context = context

    def __repr__(self):
        return "<%s - %s>" % (self.__class__.__name__, self.name)

    def render_header(self):
        return self.name


class RatingRenderer(ExtendedRenderer):
    name = "Rating"

    def render_value(self, obj):
        annotations = IAnnotations(obj)
        return len(annotations["cioppino.twothumbs.yays"])


class VotersListRenderer(ExtendedRenderer):
    name = "voters list"

    def render_value(self, obj):
        annotations = IAnnotations(obj)
        voters = []
        for voter in annotations["cioppino.twothumbs.yays"]:
            voters.append(voter)
        return voters

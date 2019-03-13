# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.component import adapts
from datetime import datetime

from plone import api
from collective.excelexport.datasources.base import BaseContentsDataSource
from zope.component import getAdapters
from ideabox.policy.export.interfaces import IUsersExportable


class UsersDataSource(BaseContentsDataSource):
    """
    Export RIC contents
    """

    adapts(Interface, Interface)

    def get_filename(self):
        return "users-%s.xls" % (datetime.now().strftime("%d-%m-%Y"))

    def get_objects(self):
        return api.user.get_users()

    def get_sheets_data(self):
        data = []
        exportables = []
        exportables.extend(self.get_exportables())
        title = "Users"
        data.append(
            {"title": title, "objects": self.get_objects(), "exportables": exportables}
        )
        return data

    def get_exportables(self):
        users = [ad[1] for ad in getAdapters((self.context,), IUsersExportable)]
        return users

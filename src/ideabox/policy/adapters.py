# -*- coding: utf-8 -*-
import datetime

from DateTime.DateTime import DateTime
from plone.app.users.browser.account import AccountPanelSchemaAdapter
from ideabox.policy.userdataschema import IEnhancedUserDataSchema


class EnhancedUserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IEnhancedUserDataSchema

    def get_birthdate(self):
        bd = self._getProperty('birthdate')
        return None if bd == DateTime('1900/01/01 00:00:00') else bd.asdatetime().date()  # noqa

    def set_birthdate(self, value):
        return self._setProperty(
            'birthdate',
            DateTime(
                datetime.datetime(
                    value.year,
                    value.month,
                    value.day,
                    0,
                    0)
            )
        )

    birthdate = property(get_birthdate, set_birthdate)

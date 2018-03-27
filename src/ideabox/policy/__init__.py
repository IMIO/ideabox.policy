# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
from cpskin.core.browser import folderview


_ = MessageFactory('ideabox.policy')

folderview.ADDABLE_TYPES += ['Link']

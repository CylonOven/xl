# -*- coding: UTF-8 -*-
# Copyright 2014-2016 Luc Saffre
#
# License: BSD (see file COPYING for details)


"""The :xfile:`models.py` module for the :mod:`lino_xl.lib.lists` app.

This module defines the tables

- :class:`List`
- :class:`Membership`

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino_xl.lib.appypod.mixins import PrintLabelsAction

from lino.api import dd
from lino import mixins


class ListType(mixins.BabelNamed):

    """Represents a possible choice for the `list_type` field of a
    :class:`List`.

    """

    class Meta:
        app_label = 'lists'
        abstract = dd.is_abstract_model(__name__, 'ListType')
        verbose_name = _("List Type")
        verbose_name_plural = _("List Types")


class ListTypes(dd.Table):
    required_roles = dd.required(OfficeStaff)
    model = 'lists.ListType'
    column_names = 'name *'


class List(mixins.BabelNamed, mixins.Referrable):

    class Meta:
        app_label = 'lists'
        abstract = dd.is_abstract_model(__name__, 'List')
        verbose_name = _("Partner List")
        verbose_name_plural = _("Partner Lists")

    list_type = dd.ForeignKey('lists.ListType', blank=True, null=True)
    remarks = models.TextField(_("Remarks"), blank=True)

    print_labels = PrintLabelsAction()


class Lists(dd.Table):
    required_roles = dd.required(OfficeUser)
    model = 'lists.List'
    column_names = 'ref name list_type *'
    order_by = ['ref']

    insert_layout = dd.InsertLayout("""
    ref list_type
    name
    remarks
    """, window_size=(60, 12))

    detail_layout = dd.DetailLayout("""
    ref list_type id
    name
    remarks
    MembersByList
    """)


class Member(mixins.Sequenced):

    class Meta:
        app_label = 'lists'
        abstract = dd.is_abstract_model(__name__, 'Member')
        verbose_name = _("List membership")
        verbose_name_plural = _("List memberships")

    list = dd.ForeignKey('lists.List')
    partner = dd.ForeignKey(
        dd.plugins.lists.partner_model,
        related_name="list_memberships")
    remark = models.CharField(_("Remark"), max_length=200, blank=True)


class Members(dd.Table):
    required_roles = dd.required(OfficeUser)
    model = 'lists.Member'


class MembersByList(Members):
    label = _("Members")
    master_key = 'list'
    order_by = ['seqno']
    column_names = "seqno partner remark workflow_buttons *"


class MembersByPartner(Members):
    master_key = 'partner'
    column_names = "list remark *"
    order_by = ['list__ref']


class AllMembers(Members):
    required_roles = dd.required(OfficeStaff)



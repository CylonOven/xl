# -*- coding: UTF-8 -*-
# Copyright 2008-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Utilities for `lino_welfare.modlib.pcsw`.

"""

from __future__ import unicode_literals
from __future__ import print_function

from django.db.models import Q

from lino.api import dd


def only_coached_by(qs, user):
    return qs.filter(coachings_by_client__user=user).distinct()


def only_coached_on(qs, period, join=None):
    """
    Add a filter to the Queryset `qs` (on model Client)
    which leaves only the clients that are (or were or will be) coached
    on the specified date.
    """
    n = 'coachings_by_client__'
    if join:
        n = join + '__' + n
    return qs.filter(only_active_coachings_filter(period, n)).distinct()


def only_active_coachings_filter(period, prefix=''):
    """
    """
    assert len(period) == 2
    args = []
    if period[0]:
        args.append(Q(
            **{prefix + 'end_date__isnull': True}) | Q(
            **{prefix + 'end_date__gte': period[0]}))
    if period[1]:
        args.append(Q(**{prefix + 'start_date__lte': period[1]}))
    return Q(*args)


def add_coachings_filter(qs, user, period, primary):
    assert period is None or len(period) == 2
    if not (user or period or primary):
        return qs
    flt = Q()
    if period:
        flt &= only_active_coachings_filter(period, 'coachings_by_client__')
    if user:
        flt &= Q(coachings_by_client__user=user)
    if primary:
        flt &= Q(coachings_by_client__primary=True)
    return qs.filter(flt).distinct()


def daterange_text(a, b):
    """
    """
    if a == b:
        return dd.dtos(a)
    return dd.dtos(a) + "-" + dd.dtos(b)


def has_contracts_filter(prefix, period):
    f1 = Q(**{prefix+'__applies_until__isnull': True})
    f1 |= Q(**{prefix+'__applies_until__gte': period[0]})
    f2 = Q(**{prefix+'__date_ended__isnull': True})
    f2 |= Q(**{prefix+'__date_ended__gte': period[0]})
    return f1 & f2 & Q(**{prefix+'__applies_from__lte': period[1]})



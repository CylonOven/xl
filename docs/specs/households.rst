.. _lino.specs.households:

=====================
The Households module
=====================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_households
    
    doctest init:

    >>> import lino
    >>> lino.startup('lino_xl.projects.max.settings.demo')
    >>> from lino.api.doctest import *

The :mod:`lino_xl.lib.households` module adds functionality for
managing households (i.e. groups of humans who live together in a same
house).

.. contents:: 
   :local:
   :depth: 2


Configuration
=============

>>> rt.show(rt.modules.households.Types)  #doctest: +REPORT_UDIFF
==== ==================== ========================= ====================== ==================== ==================== ===================== ====================
 ID   Designation          Designation (de)          Designation (fr)       Designation (et)     Designation (nl)     Designation (pt-br)   Designation (es)
---- -------------------- ------------------------- ---------------------- -------------------- -------------------- --------------------- --------------------
 1    Married couple       Ehepaar                   Couple marié           Married couple       Married couple       Married couple        Married couple
 2    Divorced couple      Geschiedenes Paar         Couple divorcé         Divorced couple      Divorced couple      Divorced couple       Divorced couple
 3    Factual household    Faktischer Haushalt       Cohabitation de fait   Factual household    Factual household    Factual household     Factual household
 4    Legal cohabitation   Legale Wohngemeinschaft   Cohabitation légale    Legal cohabitation   Legal cohabitation   Legal cohabitation    Legal cohabitation
 5    Isolated             Getrennt                  Isolé                  Isolated             Isolated             Isolated              Isolated
 6    Other                Sonstige                  Autre                  Other                Other                Other                 Other
==== ==================== ========================= ====================== ==================== ==================== ===================== ====================
<BLANKLINE>

>>> rt.show(rt.modules.households.MemberRoles)
======= ============ ===================
 value   name         text
------- ------------ -------------------
 01      head         Head of household
 02      spouse       Spouse
 03      partner      Partner
 04      cohabitant   Cohabitant
 05      child        Child
 06      relative     Relative
 07      adopted      Adopted child
 10      other        Other
======= ============ ===================
<BLANKLINE>


SiblingsByPerson
================

:class:`lino_xl.lib.households.models.SiblingsByPerson` works only
when it can determine the "one and only" current household.  

Usually this is the membership marked as `primary`.

But even when a person has multiple household memberships and none of
them is primary, it can look at the `end_date`.

>>> Person = rt.modules.contacts.Person
>>> Member = rt.modules.households.Member
>>> Member.objects.filter(end_date__isnull=False)
[Member #5 (u'Mr Paul Frisch (Head of household)'), Member #11 (u'Mr Albert Adam (Head of household)'), Member #17 (u'Mr Lars Braun (Head of household)'), Member #23 (u'Mr Ilja Adam (Head of household)')]

>>> p = Person.objects.get(first_name="Lars", last_name="Braun")
>>> Member.objects.filter(person=p).count()
2
>>> rt.show(rt.modules.households.MembersByPerson, master_instance=p)
Mr Lars Braun is
`☐  <javascript:Lino.households.Members.set_primary(null,31,{  })>`__Head of household in *Lars & Melba Braun-Frisch*
`☐  <javascript:Lino.households.Members.set_primary(null,17,{  })>`__Head of household in *Lars & Pascale Braun-Adam*
<BLANKLINE>
Create a household : **Married couple** / **Divorced couple** / **Factual household** / **Legal cohabitation** / **Isolated** / **Other**

>>> rt.show(rt.modules.households.MembersByPerson, p, nosummary=True)
=========================== =================== ========= ============ ==========
 Household                   Role                Primary   Start date   End date
--------------------------- ------------------- --------- ------------ ----------
 Lars & Melba Braun-Frisch   Head of household   No
 Lars & Pascale Braun-Adam   Head of household   No                     3/4/02
=========================== =================== ========= ============ ==========
<BLANKLINE>

>>> SiblingsByPerson = rt.modules.households.SiblingsByPerson
>>> rt.show(SiblingsByPerson, p)
================== =================== ============ ==========
 Person             Role                Start date   End date
------------------ ------------------- ------------ ----------
 Mr Lars Braun      Head of household
 Mrs Melba Frisch   Partner
================== =================== ============ ==========
<BLANKLINE>


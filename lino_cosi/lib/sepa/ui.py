# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# This file is part of Lino Cosi.
#
# Lino Cosi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Cosi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Cosi.  If not, see
# <http://www.gnu.org/licenses/>.


"""
Tables for `lino_cosi.lib.sepa`.

"""

from __future__ import unicode_literals

from lino.api import dd
from lino.modlib.contacts.roles import ContactsUser, ContactsStaff
from lino.api import dd, _, rt


class AccountsDetail(dd.FormLayout):
    main = "general"

    general = dd.Panel("""
    partner:30 iban:40 bic:20 remark:15
    sepa.StatementsByAccount
    """, label=_("Account"))


class Accounts(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'sepa.Account'
    detail_layout = AccountsDetail()


class AccountsByPartner(Accounts):
    required_roles = dd.login_required(ContactsUser)
    master_key = 'partner'
    column_names = 'iban bic remark primary *'
    order_by = ['iban']
    auto_fit_column_widths = True


class StatementDetail(dd.FormLayout):
    main = "general"

    general = dd.Panel("""
    account:30 date:40 statement_number:20 balance_start:15
    sepa.MovementsByStatement
    """, label=_("Statement"))


class Statements(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'sepa.Statement'
    column_names = 'account date statement_number balance_start balance_end *'
    order_by = ["date"]
    detail_layout = StatementDetail()
    auto_fit_column_widths = True

    # insert_layout = dd.FormLayout("""
    # account date
    # statement_number
    # balance_start balance_end
    # """, window_size=(60, 'auto'))


class StatementsByAccount(Statements):
    required_roles = dd.login_required(ContactsUser)
    master_key = 'account'
    column_names = 'date date_done statement_number balance_end'
    auto_fit_column_widths = True


class Movements(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'sepa.Movement'


class MovementsByStatement(Movements):
    required_roles = dd.login_required(ContactsUser)
    master_key = 'statement'
    column_names = 'movement_date amount partner bank_account ref'
    auto_fit_column_widths = True

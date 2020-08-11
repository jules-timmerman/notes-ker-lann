# Copyright (C) 2018-2020 by BDE ENS Paris-Saclay
# SPDX-License-Identifier: GPL-3.0-or-later

import django_tables2 as tables
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_tables2 import A
from note_kfet.middlewares import get_current_authenticated_user
from permission.backends import PermissionBackend

from .models import WEIClub, WEIRegistration, Bus, BusTeam, WEIMembership


class WEITable(tables.Table):
    """
    List all WEI.
    """
    class Meta:
        attrs = {
            'class': 'table table-condensed table-striped table-hover'
        }
        model = WEIClub
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('name', 'year', 'date_start', 'date_end',)
        row_attrs = {
            'class': 'table-row',
            'id': lambda record: "row-" + str(record.pk),
            'data-href': lambda record: reverse_lazy('wei:wei_detail', args=(record.pk,))
        }


class WEIRegistrationTable(tables.Table):
    """
    List all WEI registrations.
    """
    user = tables.LinkColumn(
        'member:user_detail',
        args=[A('user.pk')],
    )

    edit = tables.LinkColumn(
        'wei:wei_update_registration',
        args=[A('pk')],
        verbose_name=_("Edit"),
        text=_("Edit"),
        attrs={
            'a': {
                'class': 'btn btn-warning',
                'data-turbolinks': 'false',
            }
        }
    )
    validate = tables.LinkColumn(
        'wei:validate_registration',
        args=[A('pk')],
        verbose_name=_("Validate"),
        text=_("Validate"),
        attrs={
            'th': {
                'id': 'validate-membership-header'
            },
            'a': {
                'class': 'btn btn-success',
                'data-type': 'validate-membership'
            }
        }
    )

    delete = tables.LinkColumn(
        'wei:wei_delete_registration',
        args=[A('pk')],
        verbose_name=_("delete"),
        text=_("Delete"),
        attrs={
            'th': {
                'id': 'delete-membership-header'
            },
            'a': {
                'class': 'btn btn-danger',
                'data-type': 'delete-membership'
            }
        },
    )

    def render_validate(self, record):
        hasperm = PermissionBackend.check_perm(
            get_current_authenticated_user(), "wei.add_weimembership", WEIMembership(
                club=record.wei,
                user=record.user,
                date_start=timezone.now().date(),
                date_end=timezone.now().date(),
                fee=0,
                registration=record,
            )
        )
        return _("Validate") if hasperm else format_html("<span class='no-perm'></span>")

    def render_delete(self, record):
        hasperm = PermissionBackend.check_perm(get_current_authenticated_user(), "wei.delete_weimembership", record)
        return _("Delete") if hasperm else format_html("<span class='no-perm'></span>")

    class Meta:
        attrs = {
            'class': 'table table-condensed table-striped table-hover'
        }
        model = WEIRegistration
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('user', 'user.first_name', 'user.last_name', 'first_year',)
        row_attrs = {
            'class': 'table-row',
            'id': lambda record: "row-" + str(record.pk),
            'data-href': lambda record: record.pk
        }


class WEIMembershipTable(tables.Table):
    user = tables.LinkColumn(
        'wei:wei_update_registration',
        args=[A('registration.pk')],
    )

    year = tables.Column(
        accessor=A("pk"),
        verbose_name=_("Year"),
    )

    bus = tables.LinkColumn(
        'wei:manage_bus',
        args=[A('bus.pk')],
    )

    team = tables.LinkColumn(
        'wei:manage_bus_team',
        args=[A('team.pk')],
    )

    def render_year(self, record):
        return str(record.user.profile.ens_year) + "A"

    class Meta:
        attrs = {
            'class': 'table table-condensed table-striped table-hover'
        }
        model = WEIMembership
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('user', 'user.last_name', 'user.first_name', 'registration.gender', 'user.profile.department',
                  'year', 'bus', 'team', )
        row_attrs = {
            'class': 'table-row',
            'id': lambda record: "row-" + str(record.pk),
        }


class BusTable(tables.Table):
    name = tables.LinkColumn(
        'wei:manage_bus',
        args=[A('pk')],
    )

    teams = tables.Column(
        accessor=A("teams"),
        verbose_name=_("Teams"),
        attrs={
            "td": {
                "class": "text-truncate",
            }
        }
    )

    count = tables.Column(
        verbose_name=_("Members count"),
    )

    def render_teams(self, value):
        return ", ".join(team.name for team in value.order_by('name').all())

    def render_count(self, value):
        return str(value) + " " + (str(_("members")) if value > 1 else str(_("member")))

    class Meta:
        attrs = {
            'class': 'table table-condensed table-striped table-hover'
        }
        model = Bus
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('name', 'teams', )
        row_attrs = {
            'class': 'table-row',
            'id': lambda record: "row-" + str(record.pk),
        }


class BusTeamTable(tables.Table):
    name = tables.LinkColumn(
        'wei:manage_bus_team',
        args=[A('pk')],
    )

    color = tables.Column(
        attrs={
            "td": {
                "style": lambda record: "background-color: #{:06X}; color: #{:06X};"
                                        .format(record.color, 0xFFFFFF - record.color, )
            }
        }
    )

    def render_count(self, value):
        return str(value) + " " + (str(_("members")) if value > 1 else str(_("member")))

    count = tables.Column(
        verbose_name=_("Members count"),
    )

    def render_color(self, value):
        return "#{:06X}".format(value)

    class Meta:
        attrs = {
            'class': 'table table-condensed table-striped table-hover'
        }
        model = BusTeam
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('name', 'color',)
        row_attrs = {
            'class': 'table-row',
            'id': lambda record: "row-" + str(record.pk),
            'data-href': lambda record: reverse_lazy('wei:manage_bus_team', args=(record.pk, ))
        }

# Copyright (C) 2018-2020 by BDE ENS Paris-Saclay
# SPDX-License-Identifier: GPL-3.0-or-later

from django.db import models
from django.utils.translation import gettext_lazy as _
from note.models import NoteUser, Transaction


class ActivityType(models.Model):
    """
    Type of Activity, (e.g "Pot", "Soirée Club") and associated properties.

    Activity Type are used as a search field for Activity, and determine how
    some rules about the activity:
     - Can people be invited
     - What is the entrance fee.
    """
    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
    )
    can_invite = models.BooleanField(
        verbose_name=_('can invite'),
    )
    guest_entry_fee = models.PositiveIntegerField(
        verbose_name=_('guest entry fee'),
    )

    class Meta:
        verbose_name = _("activity type")
        verbose_name_plural = _("activity types")

    def __str__(self):
        return self.name


class Activity(models.Model):
    """
    An IRL event organized by a club for other club.

    By default the invited clubs should be the Club containing all the active accounts.
    """
    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
    )

    description = models.TextField(
        verbose_name=_('description'),
    )

    activity_type = models.ForeignKey(
        ActivityType,
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name=_('type'),
    )

    organizer = models.ForeignKey(
        'member.Club',
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name=_('organizer'),
    )

    note = models.ForeignKey(
        'note.Note',
        on_delete=models.PROTECT,
        related_name='+',
        null=True,
        blank=True,
        verbose_name=_('note'),
    )

    attendees_club = models.ForeignKey(
        'member.Club',
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name=_('attendees club'),
    )

    date_start = models.DateTimeField(
        verbose_name=_('start date'),
    )

    date_end = models.DateTimeField(
        verbose_name=_('end date'),
    )

    valid = models.BooleanField(
        default=False,
        verbose_name=_('valid'),
    )

    open = models.BooleanField(
        default=False,
        verbose_name=_('open'),
    )

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")


class Entry(models.Model):
    time = models.DateTimeField(
        verbose_name=_("entry time"),
    )

    note = models.ForeignKey(
        NoteUser,
        on_delete=models.PROTECT,
        verbose_name=_("note"),
    )


class Guest(models.Model):
    """
    People who are not current members of any clubs, and are invited by someone who is a current member.
    """
    activity = models.ForeignKey(
        Activity,
        on_delete=models.PROTECT,
        related_name='+',
    )

    last_name = models.CharField(
        max_length=255,
        verbose_name=_("last name"),
    )

    first_name = models.CharField(
        max_length=255,
        verbose_name=_("first name"),
    )

    inviter = models.ForeignKey(
        NoteUser,
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name=_("inviter"),
    )

    entry = models.OneToOneField(
        Entry,
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        verbose_name = _("guest")
        verbose_name_plural = _("guests")


class GuestTransaction(Transaction):
    guest = models.OneToOneField(
        Guest,
        on_delete=models.PROTECT,
    )

    @property
    def type(self):
        return _('Invitation')

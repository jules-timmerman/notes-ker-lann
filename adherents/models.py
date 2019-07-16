# -*- mode: python; coding: utf-8 -*-
# Copyright (C) 2018-2019 by BDE ENS Paris-Saclay
# SPDX-License-Identifier: GPL-3.0-or-later

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """
    An user profile

    We do not want to patch the Django Contrib Auth User class
    so this model add an user profile with additional information.
    """
    GENRES = [
        (None, "ND"),
        ("M", "M"),
        ("F", "F"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    avatar = models.ImageField(
        max_length=255,
        blank=True,
        verbose_name=_('profile picture'),
    )
    phone_number = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        default='',
        verbose_name=_('phone number'),
    )
    section = models.CharField(
        max_length=255,
        verbose_name=_('section'),
        help_text=_('e.g. "1A0", "9A♥", "SAPHIRE"'),
    )
    genre = models.CharField(
        max_length=1,
        blank=False,
        null=False,
        choices=GENRES,
        default=None,
    )
    address = models.TextField(
        blank=True,
        null=False,
        default='',
    )
    paid = models.BooleanField(
        verbose_name=_("paid"),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_("is active"),
        default=True,
    )
    is_deleted = models.BooleanField(
        verbose_name=_("is deleted"),
        default=False,
    )

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profile')

    def __str__(self):
        return self.user.get_username()


class MembershipFee(models.Model):
    """
    User can become member by paying a membership fee
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    date = models.DateField(
        max_length=255,
        verbose_name=_('date'),
    )
    amount = models.DecimalField(
        max_digits=5,  # Max 999.99 €
        decimal_places=2,
        verbose_name=_('amount'),
    )

    class Meta:
        verbose_name = _('membership fee')
        verbose_name_plural = _('membership fees')

    def __str__(self):
        return self.user.get_username()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **_kwargs):
    """
    Hook to save an user profile when an user is updated
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

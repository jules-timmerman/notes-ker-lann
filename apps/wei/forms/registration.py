# Copyright (C) 2018-2020 by BDE ENS Paris-Saclay
# SPDX-License-Identifier: GPL-3.0-or-later

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from note_kfet.inputs import AmountInput, DatePickerInput, Autocomplete, ColorWidget

from ..models import WEIClub, WEIRegistration, Bus, BusTeam, WEIMembership, WEIRole


class WEIForm(forms.ModelForm):
    class Meta:
        model = WEIClub
        exclude = ('parent_club', 'require_memberships', 'membership_duration', )
        widgets = {
            "membership_fee_paid": AmountInput(),
            "membership_fee_unpaid": AmountInput(),
            "membership_start": DatePickerInput(),
            "membership_end": DatePickerInput(),
            "date_start": DatePickerInput(),
            "date_end": DatePickerInput(),
        }


class WEIRegistrationForm(forms.ModelForm):
    class Meta:
        model = WEIRegistration
        exclude = ('wei', )
        widgets = {
            "user": Autocomplete(
                User,
                attrs={
                    'api_url': '/api/user/',
                    'name_field': 'username',
                    'placeholder': 'Nom ...',
                },
            ),
            "birth_date": DatePickerInput(),
        }


class WEIMembershipForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(queryset=WEIRole.objects)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["team"] is not None and cleaned_data["team"].bus != cleaned_data["bus"]:
            self.add_error('bus', _("This team doesn't belong to the given team."))
        return cleaned_data

    class Meta:
        model = WEIMembership
        fields = ('roles', 'bus', 'team',)
        widgets = {
            "bus": Autocomplete(
                Bus,
                attrs={
                    'api_url': '/api/wei/bus/',
                    'placeholder': 'Bus ...',
                }
            ),
            "team": Autocomplete(
                BusTeam,
                attrs={
                    'api_url': '/api/wei/team/',
                    'placeholder': 'Équipe ...',
                }
            ),
        }


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = '__all__'
        widgets = {
            "wei": Autocomplete(
                WEIClub,
                attrs={
                    'api_url': '/api/wei/club/',
                    'placeholder': 'WEI ...',
                },
            ),
        }


class BusTeamForm(forms.ModelForm):
    class Meta:
        model = BusTeam
        fields = '__all__'
        widgets = {
            "bus": Autocomplete(
                Bus,
                attrs={
                    'api_url': '/api/wei/bus/',
                    'placeholder': 'Bus ...',
                },
            ),
            "color": ColorWidget(),
        }

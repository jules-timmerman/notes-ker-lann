# -*- mode: python; coding: utf-8 -*-
# Copyright (C) 2018-2020 by BDE ENS Paris-Saclay
# SPDX-License-Identifier: GPL-3.0-or-later

from ..models import Profile, Club, Role, Membership
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    """
    REST API Serializer for Profiles.
    The djangorestframework plugin will analyse the model `Profile` and parse all fields in the API.
    """
    class Meta:
        model = Profile
        fields = '__all__'


class ClubSerializer(serializers.ModelSerializer):
    """
    REST API Serializer for Clubs.
    The djangorestframework plugin will analyse the model `Club` and parse all fields in the API.
    """
    class Meta:
        model = Club
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    """
    REST API Serializer for Roles.
    The djangorestframework plugin will analyse the model `Role` and parse all fields in the API.
    """
    class Meta:
        model = Role
        fields = '__all__'


class MembershipSerializer(serializers.ModelSerializer):
    """
    REST API Serializer for Memberships.
    The djangorestframework plugin will analyse the model `Memberships` and parse all fields in the API.
    """
    class Meta:
        model = Membership
        fields = '__all__'

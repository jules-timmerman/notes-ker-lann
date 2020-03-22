# Copyright (C) 2018-2020 by BDE ENS Paris-Saclay
# SPDX-License-Identifier: GPL-3.0-or-later

from .views import PermissionViewSet


def register_permission_urls(router, path):
    """
    Configure router for permission REST API.
    """
    router.register(path, PermissionViewSet)

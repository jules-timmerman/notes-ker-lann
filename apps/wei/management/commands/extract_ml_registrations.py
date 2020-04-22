# Copyright (C) 2018-2020 by BDE ENS Paris-Saclay
# SPDX-License-Identifier: GPL-3.0-or-later

from django.core.management import BaseCommand
from django.db.models import Q

from ...models import WEIClub


class Command(BaseCommand):
    help = "Get mailing list registrations from the last wei. " \
           "Usage: manage.py extract_ml_registrations -t {events,art,sport}. " \
           "You can write this into a file with a pipe, then paste the document into your mail manager."

    def add_arguments(self, parser):
        parser.add_argument('--type', '-t', choices=["events", "art", "sport"], default="events",
                            help='Select the type of the mailing list (default events)')
        parser.add_argument('--year', '-y', type=int, default=None,
                            help='Select the year of the concerned WEI. Default: last year')

    def handle(self, *args, **options):
        if options["year"] is None:
            wei = WEIClub.objects.order_by('-year').first()
        else:
            wei = WEIClub.objects.filter(year=options["year"])
            if wei.exists():
                wei = wei.get()
            else:
                wei = WEIClub.objects.order_by('-year').first()
                self.stderr.write(self.style.WARNING("Warning: there was no WEI in year " + str(options["year"]) + ". "
                                                     + "Assuming the last WEI (year " + str(wei.year) + ")"))
        q = Q(ml_events_registration=True) if options["type"] == "events" else Q(ml_art_registration=True)\
            if options["type"] == "art" else Q(ml_sport_registration=True)
        registrations = wei.users.filter(q)
        for registration in registrations.all():
            self.stdout.write(registration.user.email)

# Copyright (C) 2018-2021 by BDE ENS Paris-Saclay
# SPDX-License-Identifier: GPL-3.0-or-later
import time
from random import Random

from django import forms
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from .base import WEISurvey, WEISurveyInformation, WEISurveyAlgorithm, WEIBusInformation
from ...models import Bus


# TODO: Use new words
WORDS = ['Rap', 'Retro', 'DJ', 'Rock', 'Jazz', 'Chansons Populaires', 'Chansons Paillardes', 'Pop', 'Fanfare',
         'Biere', 'Pastis', 'Vodka', 'Cocktails', 'Eau', 'Sirop', 'Jus de fruit', 'Binge Drinking', 'Rhum',
         'Eau de vie', 'Apéro', 'Morning beer', 'Huit-six', 'Jeux de societé', 'Jeux de cartes', 'Danse', 'Karaoké',
         'Bière Pong', 'Poker', 'Loup Garou', 'Films', "Jeux d'alcool", 'Sport', 'Rangées de cul', 'Chips', 'BBQ',
         'Kebab', 'Saucisse', 'Vegan', 'Vege', 'LGBTIQ+', 'Dab', 'Solitaire', 'Séducteur', 'Sociale', 'Chanteur',
         'Se lacher', 'Chill', 'Débile', 'Beauf', 'Bon enfant']


class WEISurveyForm2021(forms.Form):
    """
    Survey form for the year 2021.
    Members choose 20 words, from which we calculate the best associated bus.
    """

    word = forms.ChoiceField(
        label=_("Choose a word:"),
        widget=forms.RadioSelect(),
    )

    def set_registration(self, registration):
        """
        Filter the bus selector with the buses of the current WEI.
        """
        information = WEISurveyInformation2021(registration)
        if not information.seed:
            information.seed = int(1000 * time.time())
            information.save(registration)
            registration.save()

        rng = Random(information.seed)

        words = []
        for _ in range(information.step + 1):
            # Generate N times words
            words = [rng.choice(WORDS) for _ in range(10)]
        words = [(w, w) for w in words]
        if self.data:
            self.fields["word"].choices = [(w, w) for w in WORDS]
            if self.is_valid():
                return
        self.fields["word"].choices = words


class WEIBusInformation2021(WEIBusInformation):
    """
    For each word, the bus has a score
    """
    def __init__(self, bus):
        for word in WORDS:
            setattr(self, word, 0.0)
        super().__init__(bus)


class WEISurveyInformation2021(WEISurveyInformation):
    """
    We store the id of the selected bus. We store only the name, but is not used in the selection:
    that's only for humans that try to read data.
    """
    # Random seed that is stored at the first time to ensure that words are generated only once
    seed = 0
    step = 0

    def __init__(self, registration):
        for i in range(1, 21):
            setattr(self, "word" + str(i), None)
        super().__init__(registration)


class WEISurvey2021(WEISurvey):
    """
    Survey for the year 2021.
    """

    @classmethod
    def get_year(cls):
        return 2021

    @classmethod
    def get_survey_information_class(cls):
        return WEISurveyInformation2021

    def get_form_class(self):
        return WEISurveyForm2021

    def update_form(self, form):
        """
        Filter the bus selector with the buses of the WEI.
        """
        form.set_registration(self.registration)

    @transaction.atomic
    def form_valid(self, form):
        word = form.cleaned_data["word"]
        self.information.step += 1
        setattr(self.information, "word" + str(self.information.step), word)
        self.save()

    @classmethod
    def get_algorithm_class(cls):
        return WEISurveyAlgorithm2021

    def is_complete(self) -> bool:
        """
        The survey is complete once the bus is chosen.
        """
        return self.information.step == 20


class WEISurveyAlgorithm2021(WEISurveyAlgorithm):
    """
    The algorithm class for the year 2021.
    For now, the algorithm is quite simple: the selected bus is the chosen bus.
    TODO: Improve this algorithm.
    """

    @classmethod
    def get_survey_class(cls):
        return WEISurvey2021

    @classmethod
    def get_bus_information_class(cls):
        return WEIBusInformation2021

    def run_algorithm(self):
        for registration in self.get_registrations():
            survey = self.get_survey_class()(registration)
            rng = Random(survey.information.seed)
            survey.select_bus(rng.choice(Bus.objects.all()))
            survey.save()

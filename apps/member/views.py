#!/usr/bin/env python

# Copyright (C) 2018-2019 by BDE ENS Paris-Saclay
# SPDX-License-Identifier: GPL-3.0-or-later

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, DetailView
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .models import Profile, Club, Membership
from .forms import ProfileForm, ClubForm,MembershipForm, MemberFormSet,FormSetHelper

class UserCreateView(CreateView):
    """
    Une vue pour inscrire un utilisateur et lui créer un profile

    """
    form_class = ProfileForm
    success_url = reverse_lazy('login')
    template_name ='member/signup.html'
    second_form = UserCreationForm

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = self.second_form

        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user_profile = form.save(commit=False) # do not save to db
            user_profile.user = user
            user_profile.save()
        return super().form_valid(form)



class UserDetailView(LoginRequiredMixin,DetailView):
    model = Profile


class ClubCreateView(LoginRequiredMixin,CreateView):
    """
    Create Club
    """
    model = Club
    form_class = ClubForm

    def form_valid(self,form):
        return super().form_valid(form)
   
class ClubListView(LoginRequiredMixin,ListView):
    """
    List TransactionsTemplates
    """
    model = Club
    form_class = ClubForm

class ClubDetailView(LoginRequiredMixin,DetailView):
    model = Club

class ClubAddMemberView(LoginRequiredMixin,CreateView):
    model = Membership
    form_class = MembershipForm
    template_name = 'member/add_members.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = MemberFormSet()
        context['helper'] = FormSetHelper()
        return context
   
    def post(self,request,*args,**kwargs):
        formset = MembershipFormset(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)

    def form_valid(self,formset):
        formset.save()
        return super().form_valid(formset)

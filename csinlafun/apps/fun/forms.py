# -*- coding: utf-8 -*-
from fun.models import *
from django import forms


class CreateContactInfoForm(forms.ModelForm):
    """docstring for CreateContactInfoForm"""
    class Meta:
        model = ContactInfo
        fields = ['email', 'message']    

class CreateActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = ['is_valid', 'level']   

class EditActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = ['is_valid', 'level']   

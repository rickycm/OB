# -*- coding: utf-8 -*-
__author__ = 'ricky'

from django import forms
from models import *

class PatientForm(forms.ModelForm):
    p_codeG = forms.CharField()
    p_codeP = forms.CharField()
    p_codeA = forms.CharField()
    class Meta:
        model = patient

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"Errors")
        else:
            cleaned_data = super(PatientForm, self).clean()
        return cleaned_data



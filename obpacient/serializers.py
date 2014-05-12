__author__ = 'Aston'

from rest_framework import serializers
from models import patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = patient
        #fields = (...)

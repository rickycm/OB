# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

PSTATE = [(1, u'Due Date'), (3, u'Pregnant'), (11, u'Aborted'), (12, u'Delivered'), (13, u'c')]

class patient(models.Model):
    p_name = models.CharField(max_length=200, blank=True, null=True)
    p_code = models.CharField(max_length=20, blank=True, null=True)
    p_age = models.IntegerField(blank=True, null=True)
    p_LMP = models.DateField(blank=True, null=True)
    p_EDC = models.DateField(blank=True, null=True)
    p_diseaseHis = models.TextField(max_length=2000, blank=True, null=True)
    p_phone = models.CharField(max_length=20, blank=True, null=True)
    p_Econtact = models.CharField(max_length=20, blank=True, null=True)
    p_email = models.EmailField(max_length=1000, verbose_name='e-mail', blank=True, null=True)
    p_state = models.IntegerField(choices=PSTATE, default=1, blank=True, null=True)
    p_conception = models.DateField(blank=True, null=True)
    p_addtime = models.DateTimeField(auto_now=True, blank=True, null=True)
    doctor_id = models.CharField(max_length=20, blank=True, null=True)
    # 其实doctor_id应该与User表建立关系，如下所示。
    #doctor_id = models.ForeignKey(User, related_name='patients')
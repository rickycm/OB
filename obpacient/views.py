# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
import time
from django.utils import timezone
from django.contrib.auth.forms import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from obpacient.models import patient
from obpacient.forms import *

def login_form(request):
    username = request.POST['username']
    password = request.POST['password']
    #print("************" + username + "     " + password)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/dashboard/')
        else:
            return HttpResponseRedirect("/")
            # Return a 'disabled account' error message
    else:
        return HttpResponseRedirect("/")

@csrf_protect
def register(request):
        form = UserCreationForm()
        if request.method == 'GET':
                return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
        if request.method == 'POST':
                form = UserCreationForm(request.POST)
                if form.is_valid():
                        new_user = form.save()
                        return HttpResponseRedirect("/")

def index(request):
    #if request.user.is_authenticated():
    user = request.user
    return render_to_response("index.html", {'user': user}, context_instance=RequestContext(request))
    #return HttpResponseRedirect("/accounts/login/")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

# add patient
@login_required
@csrf_protect
def add_patient(request):

    user = request.user

    if request.method == 'GET':
        renew = request.GET.get('renew')
        if renew == 'true':
            try:
                patientId = request.GET.get('patientId')
                thisPatient = patient.objects.get(pk=patientId)
            except thisPatient.DoesNotExist:
                title = u'Error:'
                errorMessage = u"The Patient doesn't exist."
                return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title},
                                      context_instance=RequestContext(request))
            form = PatientForm(instance=thisPatient)
        else:
            form = PatientForm()
        return render_to_response('patientform.html', {'title': 'New Patient', 'form': form},
                              context_instance=RequestContext(request))
    else:
        form = PatientForm(request.POST)
        #if form.is_valid():
        if True:
            p_codeG = form.data['p_codeG']
            p_codeP = form.data['p_codeP']
            p_codeA = form.data['p_codeA']
            p_LMP_data = form.data['p_LMP']
            lmp_date = datetime.strptime(p_LMP_data, '%m/%d/%Y').date()
            #print(lmp_date)
            p_EDC_data = lmp_date + timedelta(days=280)
            p_conception_data = lmp_date + timedelta(days=14)
            #print(p_conception_data)

            p = patient.objects.create(
                p_name = form.data['p_name'],
                p_code = 'G' + p_codeG + 'P' + p_codeP + 'A' + p_codeA,
                p_age = form.data['p_age'],
                p_LMP = lmp_date,
                p_EDC = p_EDC_data,
                p_diseaseHis = form.data['p_diseaseHis'],
                p_phone = form.data['p_phone'],
                p_Econtact = form.data['p_Econtact'],
                p_email = form.data['p_email'],
                p_state = form.data['p_state'],
                p_conception = p_conception_data,
                doctor_id = user.id,
                #p_addtime = datetime.now(),
            )
            p.save()

            return HttpResponseRedirect('/patientlist/')
        else:
            return render_to_response('patientform.html', {'title': 'New Patient', 'form': form}, context_instance=RequestContext(request))


@login_required
def dashboard(request):
    user = request.user
    return render_to_response("dashboard.html", {'user': user}, context_instance=RequestContext(request))

@login_required
@csrf_protect
def list_patients(rq):
    patients =[]
    ONE_PAGE_OF_DATA = 10
    if rq.user.is_authenticated():
        user = rq.user
        try:
            curPage = int(rq.GET.get('curPage', '1'))
            allPage = int(rq.GET.get('allPage','1'))
            pageType = str(rq.GET.get('pageType', ''))
        except ValueError:
            curPage = 1
            allPage = 1
            pageType = ''

        if pageType == 'pageDown':
            curPage += 1
        elif pageType == 'pageUp':
            curPage -= 1

        startPos = (curPage - 1) * ONE_PAGE_OF_DATA
        endPos = startPos + ONE_PAGE_OF_DATA

        patients = patient.objects.filter(doctor_id=user.id, p_state__lt=10)[startPos:endPos]
        for patient_one in patients:
            edc = patient_one.p_EDC
            daynow = datetime.strptime(datetime.now().strftime('%m/%d/%Y'), '%m/%d/%Y').date()
            d = (edc - daynow).days
            if d>=0 and d<=10:
                patient_one.p_state = 3
                patient_one.save()

        if curPage == 1 and allPage == 1:
            allPostCounts = patient.objects.filter(doctor_id=user.id).count()
            allPage = allPostCounts / ONE_PAGE_OF_DATA
            remainPost = allPostCounts % ONE_PAGE_OF_DATA
            if remainPost > 0:
                allPage += 1

        return render_to_response("patientlist.html", {'title': 'Patient List', 'user': user, 'patients':patients, 'allPage':allPage, 'curPage':curPage}, context_instance=RequestContext(rq))
    return HttpResponseRedirect('/')

from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from serializers import PatientSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from permissions import IsOwner;

class PatientList(APIView):

    # 在setting文件中间配置的话，就没有必要在这个地方强制指定了。
    #renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    # 只有认证的用户才能够访问数据，具体到某个医生在代码中处理。
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # 这里每个医生访问的应该只是他自己的病人
        # 尚未考虑如何解决分页问题。
        #patients = patient.objects.filter(doctor_id=request.user.id, p_state__lt=10)
        patients = patient.objects.all();
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # 不出意外的话，医生的ID信息不会包括在提交数据中，此处需要加上。
        serializer = PatientSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientDetail(APIView):

    permission_classes = [IsOwner]

    def __get_object(self, pk):
        try:
            return patient.objects.get(pk=pk)
        except patient.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        person = self.__get_object(pk)
        serializer = PatientSerializer(person)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        person = self.__get_object(pk)
        serializer = PatientSerializer(person, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        person = self.__get_object(pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
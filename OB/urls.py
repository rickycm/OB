from django.conf.urls import patterns, include, url
from obpacient import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OB.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'obpacient.views.index'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^login_form/$', views.login_form),
    (r'^accounts/logout/$', views.logout_view),
    (r'^addpatient/$', views.add_patient),
    (r'^dashboard/$', views.dashboard),
    (r'^patientlist/$', views.list_patients),
    (r'^patients/$', views.PatientList.as_view()),
    (r'^patients/(?P<pk>[0-9]+)/$', views.PatientDetail.as_view()),
)

"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from app.views import HomeView, RegistrationView, PrivateView, PrivateEditView, PrivateDeleteView, AddCVView, \
    DetailCVView, EditCVView, DeleteCVView, ContactsView
from django.contrib.auth.views import logout, login
from settings import DEBUG, MEDIA_ROOT


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^welcome/$', TemplateView.as_view(template_name='welcome.html'), name='welcome'),
    url(r'^user/(?P<pk>\d+)/$', DetailCVView.as_view(), name='user_cv'),
    url(r'^user/(?P<pk>\d+)/add_cv/$', AddCVView.as_view(), name='add_cv'),
    url(r'^user/(?P<pk>\d+)/edit_cv/$', EditCVView.as_view(), name='edit_cv'),
    url(r'^user/(?P<pk>\d+)/delete_cv/$', DeleteCVView.as_view(), name='delete_cv'),

    url(r'^contacts/', ContactsView.as_view(), name='contacts'),
    url(r'^survey_answer/', TemplateView.as_view(template_name='answer.html'), name='answer'),

    url(r'^private/(?P<pk>\d+)/$', PrivateView.as_view(), name='private_detail'),
    url(r'^private/(?P<pk>\d+)/edit/$', PrivateEditView.as_view(), name='edit_private'),
    url(r'^private/(?P<pk>\d+)/delete/$', PrivateDeleteView.as_view(), name='delete_private'),

    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
]


if DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': MEDIA_ROOT}))
from . import views
from django.conf import settings
from django.conf.urls import url, include

urlpatterns = [
    #  /app/index
    url(r'^$', views.registre, name='registre'),

    # /app/welcome
    url(r'^welcome$', views.welcome, name='index'),

    # /app/admin/
    url(r'^admin', views.admin, name='admin'),

    # /app/admin/dashboard
    url(r'^admin/dashboard', views.dashboard, name='dashboard'),

    # /app/admin/dashboard/confirmations
    url(r'^admin/dashboard/confirmations', views.dash_confirmations, name='dash_confirmations'),

    # /app/admin/dashboard/users
    url(r'^admin/dashboard/users', views.dash_users, name='dash_users'),

    # /app/admin/dashboard/users
    url(r'^admin/dashboard/settings', views.dash_settings, name='dash_settings'),

    # /app/accounts/*
    url(r'^accounts/', include('django.contrib.auth.urls', namespace='TPMailer')),

    # /app/accounts/activate/{activation code}
    url(r'^accounts/activate/(?P<activation_mail_txt>[A-Z0-9a-z]{32})$', views.activate, name='activate'),
    url(r'^accounts/activate', views.activate, name='activate'),

    # /app/test
    url(r'^test$', views.test, name='test'),
]
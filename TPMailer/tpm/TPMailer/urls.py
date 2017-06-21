from django.conf.urls import url, include
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    # /app/index
    url(r'^$', views.registre, name='registre'),

    # /app/welcome
    url(r'^welcome$', views.welcome, name='index'),

    # /app/admin/
    url(r'^admin$', views.admin, name='admin'),

    # /app/admin/home
    url(r'^admin/dashboard', views.dashboard, name='dashboard'),

    # /app/accounts/*
    url(r'^accounts/', include('django.contrib.auth.urls', namespace='TPMailer')),

    # /app/accounts/activate/{activation code}
    url(r'^accounts/activate/(?P<activation_mail_txt>[A-Z0-9a-z]{32})$', views.activate, name='activate'),
    url(r'^accounts/activate', views.activate, name='activate'),

    # /app/test
    url(r'^test$', views.test, name='test'),
]
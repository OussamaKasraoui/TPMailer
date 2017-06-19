from django.conf.urls import url
from . import views

urlpatterns = [
    #/app/index
    url(r'^$', views.index, name='index'),

    #/app/signup
    url(r'^signup', views.signup, name='signup'),

    #/app/signin
    url(r'^signin', views.signin, name='signin'),

    #/app/signin/welcome
    url(r'^signin/welcome$', views.welcome, name='welcome'),

    #/app/signin/welcome
    url(r'^signin/failed$', views.failed, name='signin failed'),

    #/app/admin
    url(r'^admin', views.admin, name='admin panel'),

    #/app/new_user
    url(r'^new_user$', views.create_user, name='create user'),

    #/app/new_user/activate_{activation code}
    url(r'^new_user/activate_(?P<activation_mail_txt>[A-Z0-9a-z]+)$', views.activate, name='Activate account'),


    #/app/test
    url(r'^test$', views.test, name='test'),
]
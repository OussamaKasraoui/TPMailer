from builtins import len

from . import models
from . import forms
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.template import loader
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import  authenticate, login as auth_login, logout
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts


# Registre view
def registre(request):
    if request.method != 'POST':
        if request.user.is_authenticated:
            return HttpResponse(loader.get_template('TPMailer/welcome.html').render({'user': request.user},request))
        else:
            ret = HttpResponse(loader.get_template('TPMailer/registre.html').render({'form': forms.UserForm}, request))
    else:
        first_name = str(request.POST['first_name'])
        last_name = str(request.POST['last_name'])
        username = str(request.POST['username'])
        email = str(request.POST['email'])
        password = str(request.POST['password'])
        password_conf = str(request.POST['confirm_password'])
        error = []


        #  Checking if values are equal and have the same length
        if password == password_conf and len(password) == len(password_conf):
            try:
                password_validators_help_texts(validate_password(password))

            except ValidationError as v:
                for er in v:
                    error.append(er)
                pass
        else:
            error = ['Password and Confirm Password aren\'t match !',]

        # if cridentials are valide
        if len(error) is 0:
            # is USERNAME and EMAIL are unique
            if is_username(username) is False and is_email(email) is False:
                # user & confirmation instance
                con = models.Confirmation()
                usr = models.User()

                #-- Creating new user--#

                # setting usr cridentials
                usr.first_name = first_name
                usr.last_name = last_name
                usr.username = username
                usr.email = email
                usr.password = make_password(password)

                # setting usr permissions
                usr.is_active = False
                usr.is_staff = False
                usr.is_superuser = False

                # saving to database
                usr.save()

                #-- Creating new checking email Object --#
                con.user_id = models.User.objects.get(pk=usr.pk)
                con.msg_txt = get_random_string(length=32,
                                                allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                con.save()

                #sending verification email
                send_mail(
                    'Activate your account',                                        # Email title here
                    '127.0.0.1:8000/app/accounts/activate/{0}'.format(con.msg_txt), # Email body here
                    settings.EMAIL_HOST_USER,                                       # Sender
                    [email],                                                        # Reciever
                    fail_silently=False                                             # tell if something goes wrong
                    )

                ret = HttpResponse(loader.get_template('TPMailer/info.html').render({'alert_type': 'info',
                                                                                     'alert_head': 'Attention ',
                                                                                     'alert_body': '{0}\'s account is created, but ...'.format(username),
                                                                                     'alert_corp': 'An email with a Linkt of activation is sent to \'{0}\', '
                                                                                                   'check it and activate your account please to be able to LOGIN'.format(email),
                                                                                     'redirect_to': settings.LOGIN_URL,
                                                                                     'redirect_text': 'Login page'
                                                                                     }))
            else:
                ret = HttpResponse(loader.get_template('TPMailer/info.html').render({'alert_type': 'danger',
                                                                                     'alert_head': 'Caution',
                                                                                     'alert_body': 'Invalid Email or username',
                                                                                     'alert_corp': 'Either username or email you supplied is already taken, choose another one please ',
                                                                                     'redirect_to': '/app/',
                                                                                     'redirect_text': 'Registre page'
                                                                                     }))
        else:
            #implement form with recent submit values
            ret = HttpResponse(loader.get_template('TPMailer/registre.html').render({
                'form': forms.UserForm(initial={
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username,
                    'email': email}),
                'error': error,
                'method': request.method}, request))

    return ret


    #Check if a username is already existes

# Check if a username is already existes
def is_username(username):
    return any(usr[0] == username for usr in models.User.objects.values_list('username'))

# Check if an email is already existes
def is_email(email):
    return any(eml[0] == email for eml in models.User.objects.values_list('email'))


@login_required     # Welcome view
def welcome(request):
    return HttpResponse(loader.get_template('TPMailer/welcome.html').render({'user': request.user}, request))

# Account activation view
def activate(request, activation_mail_txt=None):
    if request.method == 'GET':
        if activation_mail_txt is not None and is_token(activation_mail_txt):
            mail_obj = models.Confirmation.objects.get(msg_txt=activation_mail_txt)

            if mail_obj.is_checked is False:
                mail_obj.is_checked = True
                mail_obj.save()
                user = models.User.objects.get(username=mail_obj.user_id)
                user.is_active = True
                user.last_login = timezone.now()
                user.save()

                ret = HttpResponse(loader.get_template('TPMailer/info.html').render({'alert_type': 'success',
                                                                                     'alert_head': 'Success',
                                                                                     'alert_body': 'Activation Succeed',
                                                                                     'alert_corp': 'Congratulations, {0}\'s account is activated'.format(user.username),
                                                                                     'redirect_to': settings.LOGIN_URL,
                                                                                     'redirect_text': 'Login page'}))

            else:
                ret = HttpResponse(loader.get_template('TPMailer/info.html').render({'alert_type': 'warning',
                                                                                     'alert_head': 'Warning',
                                                                                     'alert_body': 'Token used',
                                                                                     'alert_corp': 'Token is already activated',
                                                                                     'redirect_to': settings.LOGIN_URL,
                                                                                     'redirect_text': 'Login page'}))
        else:
            ret = HttpResponse(loader.get_template('TPMailer/info.html').render({'alert_type': 'danger',
                                                                                 'alert_head': 'Danger',
                                                                                 'alert_body': 'Bad Token',
                                                                                 'alert_corp': '" {0} " is NOT a valid Token'.format(activation_mail_txt),
                                                                                 'redirect_to': '/app/',
                                                                                 'redirect_text': 'Home pge'}))
    else:
        ret = HttpResponse(loader.get_template('TPMailer/info.html').render({'alert_type': 'warning',
                                                                             'alert_head': 'Warning',
                                                                             'alert_body': 'Bad Request',
                                                                             'alert_corp': 'The current request is {0}, it is recommended to be GET'.format(request.method),
                                                                             'redirect_to': '/app/',
                                                                             'redirect_text': 'Home page'}))
    return ret

# check if Accout Activaton token is existe
def is_token(token):
    return any(tkn[0] == token for tkn in models.Confirmation.objects.values_list('msg_txt'))


def test(request):
    if request.user.is_authenticated:
        return HttpResponse('yse is authenticated : {0}'.format(request.user))
    else:
        return HttpResponse('No is NOT authenticated : {0}'.format(request.user))
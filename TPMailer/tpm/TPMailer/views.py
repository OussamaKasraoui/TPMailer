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
            if is_existe_username(username) is False and is_existe_email(email) is False:
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

                ret = redirect(settings.LOGIN_URL)
            else:
                ret = HttpResponse(loader.get_template('TPMailer/error.html').render({'error_message': 'registration failed',
                                                                                      'error_corp': 'either the Email or Username are already used'}))
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
def is_existe_username(username):
    return any(usr[0] == username for usr in models.User.objects.values_list('username'))

# Check if an email is already existes
def is_existe_email(email):
    return any(eml[0] == email for eml in models.User.objects.values_list('email'))


@login_required     # Welcome view
def welcome(request):
    return HttpResponse(loader.get_template('TPMailer/welcome.html').render({'user': request.user}, request))

# Account activation view
def activate(request, activation_mail_txt=None):
    if request.method == 'GET':
        if activation_mail_txt is not None:
            try:
                mail_obj = models.Confirmation.objects.get(msg_txt=activation_mail_txt)

                print('user is {0}'.format(mail_obj.user_id))

                if mail_obj.is_checked is False:
                    mail_obj.is_checked = True
                    mail_obj.save()
                    user = models.User.objects.get(username=mail_obj.user_id)
                    user.is_active = True
                    user.last_login = timezone.now()
                    user.save()
                    ret = HttpResponse(loader.get_template('TPMailer/login.html').render({'cntx': True,
                                                                                           'cntx_type': 'success',
                                                                                           'cntx_msg': '{0}\'s account is activated'.format(user.username)}))

                else:
                    ret = HttpResponse(loader.get_template('TPMailer/error.html').render({'error_message': 'Invalid request',
                                                                                           'error_corp': 'account is already activated'}))
            except:
                ret = HttpResponse(loader.get_template('TPMailer/error.html').render({'error_message': 'invalid token',
                                                                                       'error_corp': 'the token [ {0} ] wsn\'t found ! '.format(activation_mail_txt)}))
        else:
            ret = HttpResponse(loader.get_template('TPMailer/error.html').render({'error_message': 'token is messing',
                                                                                   'error_corp': 'the activation token is not supplied at all '}))
    else:
        ret = HttpResponse(loader.get_template('TPMailer/error.html').render({'error_message': 'Invalid reequest',
                                                                               'error_corp': 'the actual request is POST, it must be GET '}))
    return ret

def test(request):
    if request.user.is_authenticated:
        return HttpResponse('yse is authenticated : {0}'.format(request.user))
    else:
        return HttpResponse('No is NOT authenticated : {0}'.format(request.user))

"""
# login view
def login(request, user='to login panel'):

    if request.user.is_authenticated:
        
        if request.method == "POST":

            username = request.POST.get('email_field')
            password = request.POST.get('password_field')


            usr = authenticate(request, username=username, password=password)


            if usr != None:
                login(request, template='' )
                ret = HttpResponse(loader.get_template('TPMailer/welcome.html').render({'user': username}, request))
            else:
                ret = HttpResponse(loader.get_template('TPMailer/failed.html').render({'user': username}, request))
        else:
            template = loader.get_template('TPMailer/signin.html')
            context = {'user': user}
            ret = HttpResponse(template.render(context, request))

    return ret


# if login failed
def failed(request):
    return HttpResponse(loader.get_template('TPMailer/failed.html').render({}, request))

# account activating function
def activate(request, activation_mail_txt):
    if(len(activation_mail_txt) is 32):
        code = get_object_or_404(models.Confirmation, msg_txt = activation_mail_txt)
        if code.ischecked is False :
            code.ischecked = True
            #return
        else:
            context = 'email is already activated'
            #return

    else:
        print('world')
    return HttpResponse('activation code is {0}'.format(activation_mail_txt))

#
def admin(request):
    template = loader.get_template('TPMailer/admin.html')
    return HttpResponse(template.render({}, request))


def test(request):
    users = models.User.objects.values_list('username')
    return HttpResponse(any(usr[0] == 'alex.popo' for usr in users))
"""
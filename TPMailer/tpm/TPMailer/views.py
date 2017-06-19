from builtins import len

from . import models
from . import forms
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password, _password_validators_help_text_html
from django.contrib.auth.decorators import login_required

# index view
def index(request):
    return signup(request)

# signup view
def signup(request):
    return HttpResponse(loader.get_template('TPMailer/signup.html').render({'form': forms.UserForm}, request))

# registre a new user to database
def create_user(request):

    first_name = str(request.POST['first_name'])
    last_name = str(request.POST['last_name'])
    username = str(request.POST['username'])
    email = str(request.POST['email'])
    password = str(request.POST['password'])
    password_conf = str(request.POST['confirm_password'])

    #  Checking if values are equal and have the same length
    if password == password_conf and len(password) == len(password_conf):
        try:
            _password_validators_help_text_html(validate_password(password))

        except ValidationError as v:
            for r in v:
                error = str(error) + '<li>' + str(r) + '</li><br>'
            pass
    else:
        error = '<li><strong>Caution</strong> Password and Confirm Password aren\'t match !</li>'

    # if password field and Confirm password field are the same
    if error == None:

        if is_existe_username(username) is False and is_existe_email(email) is False:
            # user & confirmation instance
            con = models.Confirmation()
            usr = models.User()

            # Creating new checking email Object
            con.msg_txt = get_random_string(length=32,
                                            allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            con.save()

            #-- Creating new user--#

            # setting usr cridentials
            usr.first_name = first_name
            usr.last_name = last_name
            usr.username = username
            usr.email = email
            usr.password = make_password(password)
            usr.confirmation = models.Confirmation.objects.get(pk=con.pk)

            # setting usr permissions
            usr.is_active = False
            usr.is_staff = False
            usr.is_superuser = False

            # saving to database
            usr.save()

            #sending verification email
            send_mail(
                    'Activate your account',                                        #Email title here
                    '127.0.0.1:8080/new_user/activate_{0}'.format(con.msg_txt),     #Email body here
                    settings.EMAIL_HOST_USER,                                       #Sender
                    [email],                                                        #Reciever
                    fail_silently=False,                                            #tell if something goes wrong
                )

            ret = HttpResponse(loader.get_template('TPMailer/signin.html').render({'user': usr.username}, request))
        else:
            ret = HttpResponse(loader.get_template('TPMailer/error.html').render({'message_ml': email,
                                                                                  'emails': email,
                                                                                  'message_us': username,
                                                                                  'users': username}))
    else:
        ret = HttpResponse(loader.get_template('TPMailer/signup.html').render({
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

# login view
def signin(request, user='to login panel'):

    if request.method == "POST":

        username = request.POST.get('username_field')
        password = request.POST.get('password_field')

        usr = authenticate(request, username=username, password=password)

        if usr is not None:
            login(request, usr, backend=True)
            ret = HttpResponse(loader.get_template('TPMailer/welcome.html').render({'user': username}, request))
        else:
            ret = HttpResponse(loader.get_template('TPMailer/failed.html').render({'user': username}, request))
    else:
        template = loader.get_template('TPMailer/signin.html')
        context = {'user': user}
        ret = HttpResponse(template.render(context, request))

    return ret


# Welcom page
#@login_required
def welcome(request):
    return HttpResponse(loader.get_template('TPMailer/welcome.html').render({'user': request.user}, request))

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

from . import models

def dashboard(request):

    return


#@dajaxice_register(method='GET', name='Djx.confirmations')
def dash_confirmations(request):
    table_header = ['ID', 'USER', 'DATE', 'VALUE', 'STATUS']
    confs = list(models.Confirmation.objects.extra(select={'Q': 'V'}).values('pk', 'user_id', 'gen_date', 'msg_txt', 'is_checked'))
    return ({'view': True, 'table_body': confs, 'table_header': table_header})


#@dajaxice_register(method='GET', name='Djx.users')
def dash_users(request):
    #USERS QUEUE TABLE
    table_header = ['ID', 'First Name', 'Last Name', 'Username', 'Email', 'Status']
    confs = list(models.User.objects.extra(select={'Q': 'V'}).values('pk',
                                                                     'first_name',
                                                                     'last_name',
                                                                     'username',
                                                                     'email',
                                                                     'is_active'))
    return ({'view': True,
                       'table_body': confs,
                       'table_header': table_header})



#@dajaxice_register(method='GET', name='Djx.settings')
def dash_settings(request):
    #SETTINGS VIEW
    return True


def alert_example(request):
    dajax = Dajax()
    dajax.alert('Hello from python!')
    return dajax.json
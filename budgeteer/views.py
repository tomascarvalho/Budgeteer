from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Transaction, Account, Objective
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import decimal
from django.utils.translation import ugettext as _


def index(request):
    """The index function.
    This is the function that renders the first page a user will see when they arrive to the website.
    It has information about the service we provide
    Keyword arguments:
    request -- the django request object
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')

    return render(request, 'budgeteer/index.html')


def log_in(request):
    """The log_in function.
    This function receives the user email and password in the request (POST).
    Tries to fetch the user from the database, if the user doesnt exist throws an Exception
    and returns an error message.
    If the user exists it tries to authenticate the user with the usarname/password.
    Logs in the user in case of success and redirects to the dashboard.
    In case of insuccess it returns an error message.
    Keyword arguments:
    request -- the django request object that contains the user email and password that we want to authenticate
    """
    email = request.POST.get('email')
    try:
        try_user = User.objects.get(email=email)
    except (KeyError, User.DoesNotExist):
        # Translators: This error message appears on the login form in case of error
        error_message = _("Invalid Login")
        return render(request, 'budgeteer/index.html', {
            'error_message': error_message,
        })
    user_password = request.POST.get('password')
    user = authenticate(username=try_user.username, password=user_password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/dashboard')
    else:
        # Translators: This error message appears on the login form in case of error
        error_message = _("Invalid Login")
        return render(request, 'budgeteer/index.html', {
            'error_message': error_message,
        })



def signup(request):
    """The signup function.
    This function receives the user username, email, password and password confirmation in the request POST.
    Tries to fetch the user from the database, if the user exists returns an error message.
    If the user doesn't exist it tries to create a new user.
    Logs in the user in case of success and redirects to the dashboard.
    In case of insuccess it returns an error message.
    Keyword arguments:
    request -- the django request object that contains the user username, email, password and password confirmation that we want to create.
    """
    try:
        username = User.objects.get(name = request.POST['name'])
    except (KeyError, User.DoesNotExist):
        if (request.POST['s_password'] == request.POST['reenterpassword']):
            user = User.objects.create_user(request.POST.get('username', False), request.POST.get('email', False), request.POST.get('s_password', False))
            login(request, user)
            return HttpResponseRedirect('/dashboard')
    else:
        # Translators: This error message appears on the signup form in case the email is already in use
        error_message = _("Email already in use")
        return render(request, 'budgeteer/index.html', {
            'error_message': error_message,
        })
    # Translators: This error message appears on the signup form in case the user doesnt type two matchin passwords
    error_message = _("Passwords don't match")
    return render(request, 'budgeteer/index.html', {
        'error_message': error_message,
    })

def log_out(request):
    """The log_out function.
    Logs out the user from the session.
    Redirects to the index.
    Keyword arguments:
    request -- the django request object.
    """
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def new_transaction(request):
    """The new_transaction function.
    User log in is required. It redirects to the index in case the user is not logged in.
    Receives the new transaction details in the request and creates a new transaction.
    Saves it in the database and redirects the user to the dashboard.
    Keyword arguments:
    request -- the django request object that contains information of the transaction that we want to create.
    """
    t_user = User.objects.get(pk = request.user.id)
    t_amount = decimal.Decimal(request.POST['amount'])
    t_description = request.POST['description']
    t_account = Account.objects.get(pk = request.POST['account'])
    t_date = request.POST['date']
    new_transaction = Transaction(account = t_account, user= t_user, description = t_description, amount = t_amount, date = t_date)
    new_transaction.save()
    t_account.balance = t_account.balance + t_amount
    t_account.save()

    return HttpResponseRedirect('/dashboard/')


@login_required
def dashboard(request):
    """The dashboard function.
    User log in is required. It redirects to the index in case the user is not logged in.
    Function that renders the dashboard page.
    Gets the user accounts and transactions from the database.
    It then calculates the user total_balance.
    Sends the objects fetched in the context variable to the template.
    Keyword arguments:
    request -- the django request object.
    """
    user = request.user
    all_accounts = Account.objects.filter(user= user.id).order_by('name')
    total_balance = 0
    for a in all_accounts:
        total_balance = float(total_balance) + float(a.balance)

    last_month = datetime.today() - timedelta(days=30)
    last_transactions = Transaction.objects.filter(date__gte=last_month, user = user.id).order_by('-date')


    context = {
        'last_transactions': last_transactions,
        'user_accounts':all_accounts,
        'user_balance': "%0.2f"%total_balance
        }
    return render(request, 'budgeteer/dashboard.html', context)


@login_required
def manage_accounts(request):
    """The manage_accounts function.
    User log in is required. It redirects to the index in case the user is not logged in.
    Function that renders the account management page.
    Gets the user accounts from the database.
    Sends the objects fetched in the context variable to the template.
    Keyword arguments:
    request -- the django request object.
    """
    user = request.user
    user_accounts = Account.objects.filter(user=user.id).order_by('name')
    context = {'user_accounts': user_accounts}
    return render(request, 'budgeteer/manageAccounts.html', context)


@login_required
def new_account(request):
    """The new_account function.
    User log in is required. It redirects to the index in case the user is not logged in.
    Function that creates a new account.
    Receives the account information in a POST request.
    Creates a new account and saves it in the database.
    Redirects to the manage accounts page.
    Keyword arguments:
    request -- the django request object.
    """
    user = request.user
    my_user = User.objects.get(pk = user.id)
    a_amount = decimal.Decimal(request.POST['balance'])
    a_description = request.POST['description']
    a_name = request.POST['accName']
    new_account = Account(user = my_user, name = a_name, description = a_description, balance = a_amount)
    new_account.save()
    return HttpResponseRedirect('/manageAccounts/')


@login_required
def del_account(request):
    """The del_account function.
    User log in is required. It redirects to the index in case the user is not logged in.
    Function that deletes an account.
    Gets the account id through POST request and tries to fetch the account from the database.
    Throws a Account.DoesNotExist exception in case of failure and redirects to manage accounts.
    Checks if the user owns the account.
    Deletes the account.
    Redirects to manage accounts page.
    Keyword arguments:
    request -- the django request object which contains the account id in the POST request.
    """
    user = request.user
    try:
        my_user = User.objects.get(pk = user.id)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect('/manageAccounts')

    a_id = request.POST['acc_id']
    try:
        account_to_delete = Account.objects.get(pk = a_id)
    except (KeyError, Account.DoesNotExist):
        return HttpResponseRedirect('/manageAccounts')

    if (account_to_delete.user != my_user or account_to_delete == None):
        return HttpResponseRedirect('/manageAccounts')
    else:
        account_to_delete.delete()
    return HttpResponseRedirect('/manageAccounts')


@login_required
def account(request, account_id):
    """The account function.
    User log in is required. It redirects to the index in case the user is not logged in.
    Function that renders the account detail page.
    Gets the user account from the database and checks if the user ownes it.
    In case of failure redirects to manage accounts page
    Sends the objects fetched in the context variable to the template.
    Keyword arguments:
    request -- the django request object.
    account_id -- the account id.
    """
    user = request.user
    try:
        my_user = User.objects.get(pk= user.id)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect('/manageAccounts')

    try:
        account_to_edit = Account.objects.get(pk = account_id)
    except (KeyError, Account.DoesNotExist):
        return HttpResponseRedirect('/manageAccounts')
    if (account_to_edit.user != my_user):
        return HttpResponseRedirect('/manageAccounts')
    context = {
        'account': account_to_edit,
    }
    return render(request, 'budgeteer/editAccount.html', context)


@login_required
def edit_account(request, account_id):
    """The edit_account function.
    User log in is required. It redirects to the index in case the user is not logged in.
    Function that allows the user to edit an account.
    Gets the user account from the database and checks if the user ownes it.
    In case of failure redirects to manage accounts page
    Edits the account according to the desired data.
    Saves the account in the database.
    Redirects the user to the manage accounts page.
    Keyword arguments:
    request -- the django request object.
    account_id -- the account id.
    """
    user = request.user
    try:
        my_user = User.objects.get(pk= user.id)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect('/manageAccounts')

    try:
        account_to_edit = Account.objects.get(pk = account_id)
    except (KeyError, Account.DoesNotExist):
        return HttpResponseRedirect('/manageAccounts')
    else:
        if (account_to_edit.user != my_user):
            return HttpResponseRedirect('/manageAccounts')
        account_to_edit.name = request.POST['accName']
        account_to_edit.description = request.POST['description']
        account_to_edit.balance = decimal.Decimal(request.POST['balance'])
        account_to_edit.save()
    return HttpResponseRedirect('/manageAccounts')


@login_required
def manage_objectives(request):
    """The manage_objectives function.
    User log in is required. It redirects to the index in case the user is not logged in.
    Function that renders the account management page.
    Gets the user accounts from the database.
    Sends the objects fetched in the context variable to the template.
    Keyword arguments:
    request -- the django request object.
    """
    user = request.user
    user_objectives = Objective.objects.filter(user = user.id).order_by('deadline')
    username = User.objects.get(id = user.id)
    user_accounts = Account.objects.filter(user = user.id).order_by('name')

    if user_objectives is not None:
        for objective in user_objectives:
            if objective.deadline <= datetime.date(datetime.today()):
                if objective.objective == 'Spend':
                    money_spent = 0.0
                    money_spent = decimal.Decimal(money_spent)
                    try:
                        user_transactions = Transaction.objects.filter(user = username)
                    except (KeyError, Transaction.DoesNotExist):
                        return HttpResponseRedirect('/manageObjectives')
                    for transaction in user_transactions:
                        if transaction.account == objective.account:
                            money_spent = money_spent + decimal.Decimal(transaction.amount)
                    if (money_spent > objective.amount):
                        objective.completed = 'N'
                        objective.save()
                    else:
                        objective.completed = 'Y'
                        objective.save()
                elif objective.objective == 'Have':
                    if (objective.account.balance > objective.amount):
                        objective.completed = 'Y'
                        objective.save()
                    else:
                        objective.completed = 'N'
                        objective.save()

    context = {
        'user_objectives': user_objectives,
        'user_accounts': user_accounts,
        }
    return render(request, 'budgeteer/manageObjectives.html', context)



@login_required
def new_objective(request):
    """The new_objective function.
    User log in is required. It redirects to the index in case the user is not logged in.
    Function that creates a new objective.
    Receives the objective information in a POST request.
    Generate an objective description according to the information and translate it according to user language.
    Creates a new objective and saves it in the database.
    Redirects to the manage objective page.
    Keyword arguments:
    request -- the django request object.
    """
    user = request.user
    try:
        my_user = User.objects.get(pk = user.id)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect('/manageObjectives')
    o_name = request.POST['name']
    o_amount = request.POST['amount']
    o_account = int(request.POST['account'])
    o_deadline = request.POST['deadline']
    o_option = request.POST['option']
    try:
        account = Account.objects.get(id = o_account)
    except (KeyError, Account.DoesNotExist):
        return HttpResponseRedirect('/manageObjectives')
    if o_option == "Spend":
        # Translators: Translating the description that is created with base on the objective that the user picked
        o_description = _("Don't spend more than ") + str(o_amount) +_("eur from ") + account.name + _(" account")
    elif o_option == "Have":
        # Translators: Translating the description that is created with base on the objective that the user picked
        o_description = _("Have more than ")+str(o_amount) +_("eur in ") + account.name + _(" account")
    new_objective = Objective(user = my_user, account = account, name = o_name, description = o_description, objective = o_option, amount = o_amount, deadline = o_deadline)
    new_objective.save()
    return HttpResponseRedirect('/manageObjectives')



@login_required
def del_objective(request):
    """The del_objective function.
    User log in is required. It redirects to the index in case the user is not logged in.
    Function that deletes an objective.
    Gets the objective id through POST request and tries to fetch the objective from the database.
    Throws a Objective.DoesNotExist exception in case of failure and redirects to manage objectives.
    Checks if the user owns the objective.
    Deletes the objective.
    Redirects to manage objectives page.
    Keyword arguments:
    request -- the django request object which contains the objective id in the POST request.
    """
    user = request.user
    try:
        my_user = User.objects.get(pk = user.id)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect('/manageObjectives')

    o_id = request.POST['obj_id']
    try:
        objective_to_delete = Objective.objects.get(pk = o_id)
    except (KeyError, Objective.DoesNotExist):
        return HttpResponseRedirect('/manageObjectives')

    if (objective_to_delete.user != my_user or objective_to_delete == None):
        return HttpResponseRedirect('/manageObjectives')
    else:
        objective_to_delete.delete()
    return HttpResponseRedirect('/manageObjectives')


@login_required
def objective(request, objective_id):
    """The objective function.
    User log in is required. It redirects to the index in case the user is not logged in.
    Function that renders the objective detail page.
    Gets the user objective from the database and checks if the user ownes it.
    In case of failure redirects to manage objectives page
    Sends the objects fetched in the context variable to the template.
    Keyword arguments:
    request -- the django request object.
    objective_id -- the objective id.
    """
    user = request.user
    try:
        my_user = User.objects.get(pk= user.id)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect('/manageObjectives')

    try:
        objective_to_edit = Objective.objects.get(pk = objective_id)
    except (KeyError, Account.DoesNotExist):
        return HttpResponseRedirect('/manageObjectives')

    if (objective_to_edit.user != my_user):
        return HttpResponseRedirect('/manageObjectives')
    user_accounts = Account.objects.filter(user = user.id).order_by('name')
    context = {
        'objective': objective_to_edit,
        'user_accounts': user_accounts,
    }
    return render(request, 'budgeteer/editObjective.html', context)


@login_required
def edit_objective(request, objective_id):
    """The edit_objective function.
    User log in is required. It redirects to the index in case the user is not logged in.
    Function that allows the user to edit an objective.
    Gets the user objective from the database and checks if the user ownes it.
    In case of failure redirects the user to manage objective page
    Edits the objective according to the desired data.
    Saves the objective in the database.
    Redirects the user to the manage objectives page.
    Keyword arguments:
    request -- the django request object.
    objective_id -- the objective id.
    """
    user = request.user
    try:
        my_user = User.objects.get(pk= user.id)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect('/manageObjectives')

    try:
        objective_to_edit = Objective.objects.get(pk = objective_id)
    except (KeyError, Objective.DoesNotExist):
        return HttpResponseRedirect('/manageObjectives')
    else:
        try:
            account = Account.objects.get(pk = request.POST['account'])
        except(KeyError, Account.DoesNotExist):
            return HttpResponseRedirect('/manageObjectives')
        objective_to_edit.name = request.POST['name']
        objective_to_edit.objective = request.POST['option']
        objective_to_edit.amount = decimal.Decimal(request.POST['amount'])
        objective_to_edit.deadline = request.POST['deadline']
        objective_to_edit.completed = 'IP'
        if request.POST['option'] == "Spend":
            # Translators: Translating the description that is created with base on the objective that the user picked
            objective_to_edit.description = _("Don't spend more than ") + str(objective_to_edit.amount) + _("eur from ") + account.name + _(" account")
        elif request.POST['option'] == "Have":
            # Translators: Translating the description that is created with base on the objective that the user picked
            objective_to_edit.description = _("Have more than ")+str(objective_to_edit.amount) + _("eur in ") + account.name + _(" account")
        objective_to_edit.save()
    return HttpResponseRedirect('/manageObjectives')

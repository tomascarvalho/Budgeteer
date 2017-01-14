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
debug = 1

def index(request):
    return render(request, 'budgeteer/index.html')


def log_in(request):
    email = request.POST['email']
    try:
        username = User.objects.get(email=email).username
    except (KeyError, User.DoesNotExist):
        # Translators: This error message appears on the login form in case of error
        error_message = _("Invalid Login")
        return render(request, 'budgeteer/index.html', {
            'error_message': error_message,
        })
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/budgeteer/dashboard')
    else:
        # Translators: This error message appears on the login form in case of error
        error_message = _("Invalid Login")
        return render(request, 'budgeteer/index.html', {
            'error_message': error_message,
        })


def signup(request):
    try:
        username = User.objects.get(name = request.POST['name'])
    except (KeyError, User.DoesNotExist):
        if (request.POST['s_password'] == request.POST['reenterpassword']):
            user = User.objects.create_user(request.POST.get('username', False), request.POST.get('email', False), request.POST.get('password', False))
            login(request, user)
            return HttpResponseRedirect('/budgeteer/dashboard')
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
    logout(request)
    return HttpResponseRedirect('/budgeteer/')

@login_required
def new_transaction(request):
    t_user = User.objects.get(pk = request.user.id)
    t_amount = decimal.Decimal(request.POST['amount'])
    t_description = request.POST['description']
    t_account = Account.objects.get(pk = request.POST['account'])
    t_date = request.POST['date']
    new_transaction = Transaction(account = t_account, user= t_user, description = t_description, amount = t_amount, date = t_date)
    new_transaction.save()
    t_account.balance = t_account.balance + t_amount
    t_account.save()

    return HttpResponseRedirect('/budgeteer/dashboard/')

@login_required
def dashboard(request):
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
    user = request.user
    user_accounts = Account.objects.filter(user=user.id).order_by('name')
    context = {'user_accounts': user_accounts}
    return render(request, 'budgeteer/manageAccounts.html', context)

@login_required
def new_account(request):
    user = request.user
    my_user = User.objects.get(pk = user.id)
    a_amount = decimal.Decimal(request.POST['balance'])
    a_description = request.POST['description']
    a_name = request.POST['accName']
    new_account = Account(user = my_user, name = a_name, description = a_description, balance = a_amount)
    new_account.save()
    return HttpResponseRedirect('/budgeteer/manageAccounts')

@login_required
def del_account(request):

    user = request.user
    try:
        my_user = User.objects.get(pk = user.id)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect('/budgeteer/manageAccounts')

    a_id = request.POST['acc_id']
    try:
        account_to_delete = Account.objects.get(pk = a_id)
    except (KeyError, Account.DoesNotExist):
        return HttpResponseRedirect('/budgeteer/manageAccounts')

    if (account_to_delete.user != my_user or account_to_delete == None):
        return HttpResponseRedirect('/budgeteer/manageAccounts')
    else:
        account_to_delete.delete()
    return HttpResponseRedirect('/budgeteer/manageAccounts')

@login_required
def account(request, account_id):
    user = request.user
    try:
        my_user = User.objects.get(pk= user.id)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect('/budgeteer/manageAccounts')

    try:
        account_to_edit = Account.objects.get(pk = account_id)
    except (KeyError, Account.DoesNotExist):
        return HttpResponseRedirect('/budgeteer/manageAccounts')
    context = {
        'account': account_to_edit,
    }
    return render(request, 'budgeteer/editAccount.html', context)

@login_required
def edit_account(request, account_id):
    user = request.user
    try:
        my_user = User.objects.get(pk= user.id)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect('/budgeteer/manageAccounts')

    try:
        account_to_edit = Account.objects.get(pk = account_id)
    except (KeyError, Account.DoesNotExist):
        return HttpResponseRedirect('/budgeteer/manageAccounts')
    else:
        account_to_edit.name = request.POST['accName']
        account_to_edit.description = request.POST['description']
        account_to_edit.balance = decimal.Decimal(request.POST['balance'])
        account_to_edit.save()
    return HttpResponseRedirect('/budgeteer/manageAccounts')

@login_required
def manage_objectives(request):
    user = request.user
    user_objectives = Objective.objects.filter(user = user.id).order_by('deadline')

    user_accounts = Account.objects.filter(user = user.id).order_by('name')

    if user_objectives is not None:
        for objective in user_objectives:
            print(objective.deadline)
            print(datetime.date(datetime.today()))
            if objective.deadline <= datetime.date(datetime.today()):
                if objective.objective == 'Spend':
                    money_spent = 0.0
                    money_spent = decimal.Decimal(money_spent)
                    try:
                        user_transactions = Transaction.objects.filter(user = username)
                    except (KeyError, Transaction.DoesNotExist):
                        return HttpResponseRedirect('/budgeteer/manageObjectives')
                    for transaction in user_transactions:
                        if transaction.account == objective.account:
                            money_spent = money_spent + decimal.Decimal(transaction.amount)
                    if (money_spent > amount):
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
    user = request.user
    try:
        my_user = User.objects.get(pk = user.id)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect('/budgeteer/manageObjectives')
    o_name = request.POST['name']
    o_amount = request.POST['amount']
    o_account = int(request.POST['account'])
    o_deadline = request.POST['deadline']
    o_option = request.POST['option']
    try:
        account = Account.objects.get(id = o_account)
    except (KeyError, Account.DoesNotExist):
        return HttpResponseRedirect('/budgeteer/manageObjectives')
    if o_option == "Spend":
        # Translators: Translating the description that is created with base on the objective that the user picked
        o_description = _("Don't spend more than ") + str(o_amount) +_("eur from ") + account.name + _(" account")
    elif o_option == "Have":
        # Translators: Translating the description that is created with base on the objective that the user picked
        o_description = _("Have more than ")+str(o_amount) +_("eur in ") + account.name + _(" account")
    new_objective = Objective(user = my_user, account = account, name = o_name, description = o_description, objective = o_option, amount = o_amount, deadline = o_deadline)
    new_objective.save()
    return HttpResponseRedirect('/budgeteer/manageObjectives')

@login_required
def del_objective(request):

    user = request.user
    try:
        my_user = User.objects.get(pk = user.id)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect('/budgeteer/manageObjectives')

    o_id = request.POST['obj_id']
    try:
        objective_to_delete = Objective.objects.get(pk = o_id)
    except (KeyError, Objective.DoesNotExist):
        return HttpResponseRedirect('/budgeteer/manageObjectives')

    if (objective_to_delete.user != my_user or objective_to_delete == None):
        return HttpResponseRedirect('/budgeteer/manageObjectives')
    else:
        objective_to_delete.delete()
    return HttpResponseRedirect('/budgeteer/manageObjectives')

@login_required
def objective(request, objective_id):
    user = request.user
    try:
        my_user = User.objects.get(pk= user.id)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect('/budgeteer/manageObjectives')

    try:
        objective_to_edit = Objective.objects.get(pk = objective_id)
    except (KeyError, Account.DoesNotExist):
        return HttpResponseRedirect('/budgeteer/manageObjectives')

    user_accounts = Account.objects.filter(user = user.id).order_by('name')
    context = {
        'objective': objective_to_edit,
        'user_accounts': user_accounts,
    }
    return render(request, 'budgeteer/editObjective.html', context)

@login_required
def edit_objective(request, objective_id):
    user = request.user
    try:
        my_user = User.objects.get(pk= user.id)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect('/budgeteer/manageObjectives')

    try:
        objective_to_edit = Objective.objects.get(pk = objective_id)
    except (KeyError, Objective.DoesNotExist):
        return HttpResponseRedirect('/budgeteer/manageObjectives')
    else:
        try:
            account = Account.objects.get(pk = request.POST['account'])
        except(KeyError, Account.DoesNotExist):
            return HttpResponseRedirect('/budgeteer/manageObjectives')
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
    return HttpResponseRedirect('/budgeteer/manageObjectives')

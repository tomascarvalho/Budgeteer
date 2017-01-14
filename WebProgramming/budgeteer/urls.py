from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^dashboard/$', views.dashboard, name = 'dashboard'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^new_transaction/$', views.new_transaction, name='new_transaction'),
    url(r'^manageAccounts/$', views.manage_accounts, name = 'manageAccounts'),
    url(r'^new_account/$', views.new_account, name='new_account'),
    url(r'^del_account/$', views.del_account, name='del_account'),
    url(r'^(?P<account_id>[0-9]+)/account/$', views.account, name='account'),
    url(r'^(?P<account_id>[0-9]+)/edit_account/$', views.edit_account, name='edit_account'),
    url(r'^manageObjectives/$', views.manage_objectives, name = 'manageObjectives'),
    url(r'^new_objective/$', views.new_objective, name='new_objective'),
    url(r'^del_objective/$', views.del_objective, name='del_objective'),
    url(r'^(?P<objective_id>[0-9]+)/objective/$', views.objective, name='objective'),
    url(r'^(?P<objective_id>[0-9]+)/edit_objective/$', views.edit_objective, name='edit_objective'),
]

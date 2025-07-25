
from django.contrib import admin
from django.urls import path
from myapp import views
from myapp.views import starter, register

urlpatterns = [
    path('/', admin.site.urls),
    path('home', views.index, name='index'),
    path('starter/',views.starter,name='starter'),
    path('',views.register,name='register'),
    path('login/',views.login_view, name='login'),
    path('about/',views.about,name='about'),
    path('services/',views.services,name='services'),
    path('doctors/',views.doctors,name='doctors'),
    path('appointments/',views.appointments,name='appointments'),
    path('contacts/',views.contacts,name='contacts'),
    path('departments/',views.departments,name='departments'),
    path('dropdown/',views.dropdown,name='dropdown'),
    path('show/',views.show,name='show'),
    path('delete/<int:id>',views.delete),
    path('registration/',views.registration,name='show'),
    path('delete_Contact/<int:id>',views.delete_Contact),
    path('edit/<int:id>',views.edit,name='edit'),

             #Mpesa API urls
    path('pay/', views.pay, name='pay'),

    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),
    path('transactions/', views.transactions_list, name='transactions'),



]

import json

from django.shortcuts import render,redirect,get_object_or_404
from requests.models import HTTPBasicAuth

from myapp.credentials import LipanaMpesaPpassword, MpesaAccessToken
from myapp.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.http import HttpResponse
import requests

# Create your views here.
def index(request):
    return render(request,'index.html')
def starter(request):
    return render(request,'starter-page.html')
def about(request):
    return render(request,'about.html')
def services(request):
    return render(request,'services.html')
def doctors(request):
    return render(request,'doctors.html')

def appointments(request):
 if request.method == "POST":
     myappointments=Appointment1(
         name= request.POST['name'],
         email= request.POST['email'],
         phone= request.POST['phone'],
         datetime= request.POST['date'],
         department= request.POST['department'],
         doctors= request.POST['doctor'],
         message= request.POST['message']

        )
     myappointments.save()
     messages.success(request,'Your message has been submitted')
     return redirect('/show')

 else:
     return render(request,'appointments.html')

def contacts(request):
   if request.method=="POST":
       mycontacts= Contact(
           name=request.POST['name'],
           email=request.POST['email'],
           subject=request.POST['subject'],
           message=request.POST['message'],
       )

       mycontacts.save()
       messages.success(request,'Your contact has been submitted')
       return redirect('/contacts')

   else:

    return render(request,'contacts.html')


def departments(request):
    return render(request,'departments.html')
def dropdown(request):
    return render(request,'dropdown.html')

def show(request):
    all= Appointment1.objects.all()
    return render(request,'show.html',{'all':all})

def delete(request,id):
    myappoint = Appointment1.objects.get(id=id)
    myappoint.delete()
    return redirect('/show')

def registration(request):
    regall= Contact.objects.all()
    return render(request,'registration.html',{'regall':regall})

def delete_Contact(request,id):
    regcon =Contact.objects.get(id=id)
    regcon.delete()
    return redirect('/registration')
def edit(request,id):
    editappointment=get_object_or_404(Appointment1,id=id)

    if request.method== "POST":
        editappointment.name = request.POST.get('name')
        editappointment.email = request.POST.get('email')
        editappointment.phone = request.POST.get('phone')
        editappointment.datetime = request.POST.get('date')
        editappointment.department = request.POST.get('department')
        editappointment.doctors = request.POST.get('doctor')
        editappointment.message = request.POST.get('message')


        editappointment.save()
        messages.success(request,'Your appointment has been updated successfully')
        return redirect('/show')

    return render(request,'edit.html',{'editappointment':editappointment})

def register(request):
    """ Show the registration form """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check the password
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                # Display a message
                messages.success(request, "Account created successfully")
                return redirect('/login')
            except:
                # Display a message if the above fails
                messages.error(request, "Username already exist")
        else:
            # Display a message saying passwords don't match
            messages.error(request, "Passwords do not match")

    return render(request, 'register.html')

def login_view (request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        # Check if the user exists
        if user is not None:
            # login(request, user)
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('/home')
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'login.html')


def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
     return render(request,'pay.html')


def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/callback",
            "AccountReference": "Medilab",
            "TransactionDesc": "Appointment"
        }
        response = requests.post(api_url, json=request_data, headers=headers)

        response_data = response.json()
        transaction_id = response_data.get("CheckoutRequestID", "N/A")
        result_code = response_data.get("ResponseCode", "1")  # 0 is success, 1 is failure

        if result_code == "0":
            # Only save transaction if it was successful
            transaction = Transaction(
                phone_number=phone,
                amount=amount,
                transaction_id=transaction_id,
                status="Success"
            )
            transaction.save()

            return HttpResponse(f"Transaction ID: {transaction_id}, Status: Success")
        else:
            return HttpResponse(f"Transaction Failed. Error Code: {result_code}")


    return HttpResponse("Invalid Request")

def transactions_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'transactions.html', {'transactions': transactions})

import math
import random
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .models import Organization, Employee
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import datetime
from django.core.mail import send_mail



#pwo = PasswordGenerator()
#write your views below

#Index page
def index(request):
    return render(request, 'Index.html')


#Login Deccorator
def org_login_required(function):
    def wrapper(request, *args, **kw):
        if 'logged_in' in request.session:
            if request.session['u_type'] == 'org':
                return function(request, *args, **kw)
            else:
                messages.error(request, "You don't have privilege to access this page!")
                return HttpResponseRedirect('/')
        else:
            messages.error(request, "Logout Request/ Unauthorized Request, Please login!")
            return HttpResponseRedirect('/LoginOrg')
    return wrapper

#User Login Decorator
def user_login_required(function):
    def wrapper(request, *args, **kw):
        if 'logged_in' in request.session:
            if request.session['u_type'] == 'emp':
                return function(request, *args, **kw)
            else:
                messages.error(request, "You don't have privilege to access this page!")
                return HttpResponseRedirect('/')
        else:
            messages.error(request, "Logout Request / Unauthorized Request, Please login!")
            return HttpResponseRedirect('/LoginUser')
    return wrapper


#Organisation login function
def org_login(request):
    if request.method == "POST":
        o_email = request.POST['o_email']
        o_pass = request.POST['o_pass']
        org_details = Organization.objects.filter(o_email=o_email, o_password=o_pass).values()
        if org_details:
            request.session['logged_in'] = True
            request.session['o_email'] = org_details[0]["o_email"]
            request.session['o_id'] = org_details[0]["id"]
            request.session['o_name'] = org_details[0]["o_name"]
            request.session['u_type'] = "org"
            return HttpResponseRedirect('/org_index')
        else:
            return render(request, 'OrgLogin.html', {'details': "0"})
    else:
        return render(request, 'OrgLogin.html')

@org_login_required
def org_index(request):
    return render(request,'OrgIndex.html')

@user_login_required
def user_index(request):
    return render(request,'EmpIndex.html')

#User Login function
def user_login(request):
    if request.method == "POST":
        e_email = request.POST['e_email']
        e_pass = request.POST['e_pass']
        user_details = Employee.objects.filter(e_email=e_email, e_password=e_pass).values()
        if user_details:
            request.session['logged_in'] = True
            request.session['u_email'] = user_details[0]["e_email"]
            request.session['u_id'] = user_details[0]["id"]
            request.session['u_name'] = user_details[0]["e_name"]
            request.session['u_oid'] = user_details[0]["o_id_id"]
            request.session['u_type'] = "emp"
            return HttpResponseRedirect('/user_index')
        else:
            return render(request, 'EmpLogin.html', {'msg': "0"})
    else:
        return render(request, 'EmpLogin.html')


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(5):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

#Register User Function
def org_register(request):
    if request.method == "POST":
        try:
            o_name = request.POST['org_name']
            o_email = request.POST['o_email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            contact_no = request.POST['contact_no']
            website = request.POST['website']
            o_address = request.POST['o_address']
            
            user_obj = Organization.objects.filter(o_email=o_email)
            if user_obj.exists():
                return render(request, 'OrgRegister.html', {'error' : '1'}) 
            
            if password1 == password2:
                obj = Organization.objects.create(o_name=o_name, o_email=o_email, o_password=password1, o_contact=contact_no, o_website=website, o_address=o_address)
                obj.save()
                return HttpResponseRedirect('/LoginOrg')
            else:
                #messages.error(request, "Password not matched!")
                return render(request, 'OrgRegister.html', {'error' : '2'}) 
                #return render(request, 'OrgRegister.html')
        except Exception as e:
            return render(request, 'OrgRegister.html', {'error' : '3'})
    else:
        return render(request, 'OrgRegister.html')
    
@csrf_exempt
def logout(request):
    if request.method == 'POST':
        try:
            for key in list(request.session.keys()):
                del request.session[key]
            messages.success(request, "You are logged out successfully!")
            return HttpResponseRedirect('/')
        except:
            messages.error(request, "Some error occurred during logging out!")
            return HttpResponseRedirect('/')

#Organisation change password
def org_change_password(request):
    if request.method == 'POST':
        oldPwd = request.POST['oldPwd']
        newPwd = request.POST['newPwd']
        o_id = request.session['o_id']
        o_email = request.session['o_email']
        org_details = Organization.objects.filter(o_email=o_email, o_password=oldPwd, pk=o_id).update(o_password=newPwd)
        if org_details:
            messages.success(request, "Password Change Successfully")
            return HttpResponseRedirect('/org_index')
        else:
            messages.error(request, "Old Password was not matched!")
            return HttpResponseRedirect('/org_change_password')
    else:
        return render(request, 'OrgChangePass.html')
    
@user_login_required
def user_change_password(request):
    if request.method == 'POST':
        oldPwd = request.POST['oldPwd']
        newPwd = request.POST['newPwd']
        u_id = request.session['u_id']
        u_email = request.session['u_email']
        emp_details = Employee.objects.filter(e_email=u_email, e_password=oldPwd, pk=u_id).update(e_password=newPwd)
        if emp_details:
            messages.success(request,"Password Change Successfully")
            return HttpResponseRedirect('/user_index')
        else:
            messages.error(request, "Old Password was not matched!")
            return HttpResponseRedirect('/user_change_password')
    else:
        return render(request, 'EmpChangePass.html')
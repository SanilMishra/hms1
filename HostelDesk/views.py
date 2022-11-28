from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
# from .forms import LoginForm,SignupForm
from django.db import connection
from .models import *
from datetime import datetime, timedelta
from django.db import connection
import random

def redirect_modules(role):
    if role == 1:
        # return render(request,"admin_module.html")
        return redirect("../admin_module")
    elif role == 2:
        # return render(request,"student_module.html")
        return redirect("../student_module")
    elif role == 3:
        # return render(request,"hostel_manager_module.html")
        return redirect("../hostel_manager_module")
    elif role == 4:
        # return render(request,"mess_manager_module.html")
        return redirect("../mess_manager_module")


# Create your views here.
def index(request):
  if request.session.has_key('user'):
    #Deleting session variable
    del request.session['user']
  return render(request,"index.html")


'''****************************************************************************************************************************************************'''  

def login(request):
    dict2 = {'admin':1,'student':2,'h_manager':3,'m_manager':4}
    dict1={'name':'','password':'','role':''}
    if request.method=="POST":
        dict1=request.POST
        cursor =  connection.cursor()
        query = "select password,r_id from login_cred where u_id = '{}'"
        query = query.format(dict1['name'])
        cursor.execute(query)
        y = cursor.fetchall()
        if (len(y)!=0):
            if (y[0][0]==dict1['password'] and y[0][1]==dict2[dict1['role']]):
                role = dict2[dict1['role']]
                request.session['user'] = [dict1['name'],role]
                return redirect_modules(role)
            else:
                # print("Wrong credentials or user doesn't exist")
                return render(request, "login.html",{'error':"Wrong credentials or user doesn't exist"})
        else:
            return render(request, "login.html",{'error':"Wrong credentials or user doesn't exist"})  
    elif request.session.has_key('user'):
        # print(request.session['user']) 
        role = request.session['user'][1]
        return redirect_modules(role)
    return render(request,"login.html")



'''****************************************************************************************************************************************************''' 

def signup(request):
    # entered_details = {'name':[''],'rollno':[''],'gender':[''],'pass1':[''],'pass2':[''],'course':[''],'phno':[''],'email':[''],'pname':[''],'p_phno':['']}
    if request.method == "POST":
        entered_details = request.POST
        for i in entered_details.values():
            if i=='':
                return render(request, "signup.html",{'user_exists':'','error':'Kindly enter all values.','pass_error':""})
        if (entered_details['pass1'] != entered_details['pass2']):
            return render(request, "signup.html",{'user_exists':'','error':'','pass_error':"Passwords doesn't match."})
        else:
            cursor = connection.cursor()
            user_exists_query = "select * from login_cred where u_id = '{}'"
            user_exists_query = user_exists_query.format(entered_details['rollno'])
            # print(user_exists_query)
            cursor.execute(user_exists_query)
            user_exists = cursor.fetchall()
            print(user_exists)
            if (len(user_exists)!=0):
                return render(request, "signup.html",{'user_exists':'User already exists.','error':'','pass_error':""})
            else:
                insert_query = "insert into student_details values ('{}','{}','{}','{}',{},'{}','{}',{})"
                reg_login_query = "insert into login_cred values ('{}','{}',2)"
                insert_query = insert_query.format(entered_details['name'],
                                                    entered_details['rollno'],
                                                    entered_details['gender'],
                                                    entered_details['course'],
                                                    entered_details['phno'],
                                                    entered_details['email'],
                                                    entered_details['pname'],
                                                    entered_details['p_phno'])
                reg_login_query = reg_login_query.format(entered_details['rollno'],entered_details['pass1'])
                cursor.execute(reg_login_query)
                cursor.execute(insert_query)
                return render(request,"signup_1.html")
    return render(request,"signup.html")



'''****************************************************************************************************************************************************''' 

def admin_module(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            return render(request,"admin_module.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def student_module(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 2:
            display_name = {'name':'Profile'}
            cursor =  connection.cursor()
            query = "select name from student_details where roll_no = '{}';"
            query = query.format(user_details[0])
            cursor.execute(query)
            y = cursor.fetchall()
            if (len(y)!=0):
                display_name['name'] = y[0][0]
            # print(y)
            return render(request,"student_module.html",display_name)
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def hostel_manager_module(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 3:
            return render(request,"hostel_manager_module.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def mess_manager_module(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 4:
            return render(request,"mess_manager_module.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def ahm(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            return render(request,"ahm.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def rhm(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            return render(request,"rhm.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def amm(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            return render(request,"rhm.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def rmm(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            return render(request,"rhm.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")
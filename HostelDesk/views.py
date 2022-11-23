from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
# from .forms import LoginForm,SignupForm
from django.db import connection
from .models import *
from datetime import datetime, timedelta
from django.db import connection
import random
import csv

# Create your views here.
def index(request):
  #Company home page
  if request.session.has_key('Usr'):
    #Deleting session variable
    del request.session['Usr']
  return render(request,"index.html")

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
        # print(y)
        if (len(y)!=0):
            if (y[0][0]==dict1['password'] and y[0][1]==dict2[dict1['role']]):
                # return redirect("")
                if dict2[dict1['role']] == 1:
                    return redirect("../admin_module")
                elif dict2[dict1['role']] == 2:
                    return redirect("../student_module")
                elif dict2[dict1['role']] == 3:
                    return redirect("../hostel_manager_module")
                elif dict2[dict1['role']] == 4:
                    return redirect("../mess_manager_module")
                # print("Correct password")
            else:
                return render(request,"login.html",{"error":"Wrong credentials or user doesn't exist"})
        else:
            return render(request,"login.html",{"error":"User doesn't exist"})  
        

    return render(request,"login.html")

def signup(request):
    return render(request,"signup.html")

def admin_module(request):
    return render(request,"admin_module.html")

def student_module(request):
    return render(request,"student_module.html")

def mess_manager_module(request):
    return render(request,"mess_manager_module.html")

def hostel_manager_module(request):
    return render(request,"hostel_manager_module.html")
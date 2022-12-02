from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
# from .forms import LoginForm,SignupForm
from django.db import connection
from django.db import IntegrityError
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

def rollno_validation(rollno):
    rollno = rollno.lower()
    print(rollno)
    masters = ['ar','ch','ce','cs','ca','ee','ec','me','mt','ma','cy','ph','ms']
    bachelors = ['cs','ee','ec','me','ep','ch','ar','bt','ce','mt','pe']
    if len(rollno)==9 and rollno[0].isalpha() and rollno[1:7].isdigit() and rollno[7:10].isalpha() and rollno[0] in ['b','m'] :
        if (rollno[0]=='b' and rollno[7:] in bachelors):
            return 1
        elif (rollno[0]=='m' and rollno[7:] in masters):
            return 1
    else:
        return -1
    return -1
    
def email_validation(email,rollno):
    rollno = rollno.lower()
    mail_format = '_' + rollno + '@nitc.ac.in'
    if len(email)<= 22:
        return -1
    elif email[-21:] != mail_format:
        return -1
    else:
        return 1

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

#SIGNUP
def signup(request):
    # entered_details = {'name':[''],'rollno':[''],'gender':[''],'pass1':[''],'pass2':[''],'course':[''],'phno':[''],'email':[''],'pname':[''],'p_phno':['']}
    if request.method == "POST":
        entered_details = request.POST
        for i in entered_details.values():
            if i=='':
                return render(request, "signup.html",{'user_exists':'','error':'Kindly enter all values.','pass_error':""})
        if rollno_validation(entered_details['rollno'])== -1:
            return render(request, "signup.html",{'error':'Invalid roll number.'})
        if (entered_details['pass1'] != entered_details['pass2']):
            return render(request, "signup.html",{'user_exists':'','error':'','pass_error':"Passwords doesn't match."})
        if email_validation(entered_details['email'],entered_details['rollno'])== -1:
            return render(request, "signup.html",{'error':'Invalid institute email.'})
        else:
            cursor = connection.cursor()
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
            try:
                cursor.execute(reg_login_query)
                cursor.execute(insert_query)
            except IntegrityError:
                return render(request, "signup.html",{'user_exists':'User already exists.'})
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

'''****************************************************************************************************************************************************''' 

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
            return render(request,"student_module.html",display_name)
        else:
            return redirect("../login")
    else:
        return redirect("../login")


def application_h(request):
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
            
            if request.method=="POST":
                entered_floor = request.POST
                if len(entered_floor.keys())==1:
                    display_name['error'] = 'Kindly choose a floor.'
                    return render(request, "application_h.html",display_name)
                pfloor = entered_floor['hostel']
                return fuc(request, pfloor)
            return render(request,"application_h.html",display_name)
        else:
            return redirect("../login")
    else:
        return redirect("../login")


def application_m(request):
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
            return render(request,"application_m.html",display_name)
        else:
            return redirect("../login")
    else:
        return redirect("../login")

'''****************************************************************************************************************************************************''' 

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

'''**************************************************************************************************************************************************************'''

#APPOINT HOSTEL MANAGER
def ahm(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            if request.method == "POST":
                new_hm = request.POST
                for i in new_hm.values():
                    if i=='':
                        return render(request, "ahm.html",{'error':'Kindly enter all values.'})
                insert_query = "insert into hostel_manager values ('{}','{}','{}')"
                reg_login_query = "insert into login_cred values ('{}','{}',3)"
                insert_query = insert_query.format(new_hm['username'], new_hm['name'], new_hm['hostel'])
                reg_login_query = reg_login_query.format(new_hm['username'], new_hm['password'])
                cursor = connection.cursor()
                try:
                    cursor.execute(reg_login_query)
                    cursor.execute(insert_query)
                except IntegrityError :
                    return  render(request, "ahm.html",{'error':'User already exists.'})
                return render(request,"ahm_1.html")
            return render(request,"ahm.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

'''**************************************************************************************************************************************************************'''

#REMOVE HOSTEL MANAGER
def rhm(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            if request.method == "POST":
                remove_hm = request.POST
                # print(remove_hm)
                for i in remove_hm.values():
                    if i=='':
                        return render(request, "rhm.html",{'error':'Kindly enter all values.'})
                select_query = "select * from login_cred where u_id = '{}'"
                select_query = select_query.format(remove_hm['username'])
                remove_query = "delete from hostel_manager where hm_id = '{}'"
                remove_login_query = "delete from login_cred where u_id = '{}'"
                remove_query = remove_query.format(remove_hm['username'])
                remove_login_query = remove_login_query.format(remove_hm['username'])
                cursor = connection.cursor()
                cursor.execute(select_query)
                y = cursor.fetchall()
                if len(y)==0:
                    return render(request, "rhm.html",{'error':"User doesn't exist."})
                cursor.execute(remove_query)
                cursor.execute(remove_login_query)
                return render(request, "rhm_1.html")
            return render(request,"rhm.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

'''**************************************************************************************************************************************************************'''

#APPOINT MESS MANAGER
def amm(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            if request.method=="POST":
                new_mm = request.POST
                # print(new_mm)
                for i in new_mm.values():
                    if i=='':
                        return render(request, "amm.html",{'error':'Kindly enter all values.'})
                insert_query = "insert into mess_manager values ('{}','{}','{}')"
                reg_login_query = "insert into login_cred values ('{}','{}',4)"
                insert_query = insert_query.format(new_mm['username'], new_mm['name'], new_mm['mess'])
                reg_login_query = reg_login_query.format(new_mm['username'], new_mm['password'])
                cursor = connection.cursor()
                try:
                    cursor.execute(reg_login_query)
                    cursor.execute(insert_query)
                except IntegrityError :
                    return  render(request, "amm.html",{'error':'User already exists.'})
                return render(request,"amm_1.html")
            return render(request,"amm.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

'''**************************************************************************************************************************************************************'''

#REMOVE MESS MANAGER
def rmm(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            if request.method == "POST":
                remove_mm = request.POST
                for i in remove_mm.values():
                    if i=='':
                        return render(request, "rmm.html",{'error':'Kindly enter all values.'})
                select_query = "select * from login_cred where u_id = '{}'"
                select_query = select_query.format(remove_mm['username'])
                remove_query = "delete from mess_manager where mm_id = '{}'"
                remove_login_query = "delete from login_cred where u_id = '{}'"
                remove_query = remove_query.format(remove_mm['username'])
                remove_login_query = remove_login_query.format(remove_mm['username'])
                cursor = connection.cursor()
                cursor.execute(select_query)
                y = cursor.fetchall()
                if len(y)==0:
                    return render(request, "rmm.html",{'error':"User doesn't exist."})
                cursor.execute(remove_query)
                cursor.execute(remove_login_query)
                return render(request, "rmm_1.html")
            return render(request,"rmm.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

'''****************************************************************************************************************************************************''' 

def change_password(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if request.method=="POST":
            entered_details = request.POST
            for i in entered_details.values():
                if i=='':
                    return render(request, "change_password.html",{'error':'Kindly enter all values.'})
            if (entered_details['n_pass'] != entered_details['re_n_pass']):
                return render(request, "change_password.html",{'error':"Passwords doesn't match."})
            if (entered_details['c_pass'] == entered_details['re_n_pass'] == entered_details['n_pass']):
                return render(request, "change_password.html",{'error':"New password cannot be same as old password."})
            get_password_query = "select password from login_cred where u_id = '{}'"
            get_password_query = get_password_query.format(user_details[0])
            cursor = connection.cursor()
            cursor.execute(get_password_query)
            y = cursor.fetchall()
            if y[0][0] != entered_details['c_pass']:
                return render(request, "change_password.html",{'error':"Password incorrect."})
            else:
                change_password_query = "update login_cred set password='{}' where u_id='{}'"
                change_password_query = change_password_query.format(entered_details['n_pass'],user_details[0])
                cursor.execute(change_password_query)
                return render(request, "change_password_1.html")
        return render(request,'change_password.html')

'''****************************************************************************************************************************************************'''

def get_free_room(phostel,pfloor,rno): #integer ags
    cursor =  connection.cursor()

    query = "SELECT * FROM Student_Allocation_H WHERE Roll_No='{}'"
    query = query.format(rno)
    cursor.execute(query)
    w = cursor.fetchall()

    if len(w) > 0:
        return (-1,-2)
    
    query = "select * from Room_Details where Floor_Id='{}' and H_Id='{}' and (Status=0 or Status=1)"
    query = query.format(pfloor,phostel)
    cursor.execute(query)
    y = cursor.fetchall()
    if len(y)==0:
        query = "select * from Room_Details where H_Id='{}' and (Status=0 or Status=1)"
        query = query.format(phostel)
        cursor.execute(query)
        y = cursor.fetchall()
    if len(y)==0:
        return (-1,-1)
    else:
        query = "UPDATE Room_Details SET Status='{}' WHERE H_Id='{}' and Room_Id='{}' and Floor_Id='{}'"
        query = query.format(y[0][3]+1,y[0][0],y[0][2],y[0][1])
        cursor.execute(query)

        query = "select * from Hostel_Details where H_Id='{}'"
        query = query.format(pfloor,phostel)
        cursor.execute(query)
        z=cursor.fetchall()

        query = "UPDATE Hostel_Details SET Free_Room='{}' WHERE H_Id='{}'"
        query = query.format(z[0][2]-1,y[0][0])
        cursor.execute(query)

        query = "INSERT INTO Student_Allocation_H VALUES('{}','{}','{}','{}')"
        query = query.format(y[0][0],y[0][1],y[0][2],rno)
        cursor.execute(query)
        return (y[0][1], y[0][2])

def check(pfloor,jaba,gender):
    if (gender=="M"):
        if (jaba!=2 and jaba!=3 and pfloor>3):
            return -1
        else:
            return 0
    elif (gender=="F"):
        if (jaba==1 or jaba==4 and pfloor>3):
            return -1
        else:
            return 0

def fuc(request,pfloor):
    # stuedtn module
    rollno=request.session["user"][0]
    cursor =  connection.cursor()
    query = "select * from Student_Details where Roll_No='{}'"
    query = query.format(rollno)
    y = cursor.execute(query)
    y = cursor.fetchall()

    gender=y[0][2]
    jaba=y[0][3]
    if (check(pfloor,jaba,gender)==-1):
        return render(request, "application_h.html",{'ferror':"Choose floor between 1 to 3"})
    else:
        if (gender=='M'):
            if jaba==1:
                query = "select * from Hostel_Details where H_Id=1"
                cursor.execute(query)
                z=cursor.fetchall()

                if z[0][2]==0:
                    query = "select * from Hostel_Details where H_Id=2"
                    cursor.execute(query)
                    z=cursor.fetchall()
                if z[0][2]==0:
                    print("error room not available in a and b")
                else:
                    a,b=get_free_room(z[0][0],pfloor,rollno)

            elif jaba==2 or jaba==3:
                query = "select * from Hostel_Details where H_Id=10"
                cursor.execute(query)
                z=cursor.fetchall()
                if z[0][2]==0:
                    print("error room not available in mbh")
                else:
                    a,b=get_free_room(z[0][0],pfloor,rollno)
            elif jaba==4:
                query = "select * from Hostel_Details where H_Id=4"
                cursor.execute(query)
                z=cursor.fetchall()

                if z[0][2]==0:
                    query = "select * from Hostel_Details where H_Id=5"
                    cursor.execute(query)
                    z=cursor.fetchall()
                if z[0][2]==0:
                    query = "select * from Hostel_Details where H_Id=6"
                    cursor.execute(query)
                    z=cursor.fetchall()
                if z[0][2]==0:
                    print("error room not available in d,e,f")
                else:
                    a,b=get_free_room(z[0][0],pfloor,rollno)
            elif jaba==5:
                query = "select * from Hostel_Details where H_Id=8"
                cursor.execute(query)
                z=cursor.fetchall()
                if z[0][2]==0:
                    print("error room not available in pg1")
                else:
                    a,b=get_free_room(z[0][0],pfloor,rollno)
            elif jaba==6:
                query = "select * from Hostel_Details where H_Id=9"
                cursor.execute(query)
                z=cursor.fetchall()
                if z[0][2]==0:
                    print("error room not available in pg2")
                else:
                    a,b=get_free_room(z[0][0],pfloor,rollno)
        elif (gender=="F"):
            if jaba==1 or jaba==4:
                query = "select * from Hostel_Details where H_Id=11"
                cursor.execute(query)
                z=cursor.fetchall()
                if z[0][2]==0:
                    print("error room not available in lh")
                else:
                    a,b=get_free_room(z[0][0],pfloor,rollno)
            else:
                
                query = "select * from Hostel_Details where H_Id=12"
                cursor.execute(query)
                z=cursor.fetchall()
                if z[0][2]==0:
                    print("error room not available in mlh")
                else:
                    a,b=get_free_room(z[0][0],pfloor,rollno)          
        return render(request,"application_h_1.html")

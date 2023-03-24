from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *
from random import *
from django.core.mail import send_mail

# Create your views here.

"""
get(): return object

models.object.get(fieldname = htmlname) : fetch data from database(model).

uid = models.object.get()
uid.fieldname = newvalue
uid.save() = for update data


# to store data in model(similar like insert query)
uid = model.objects.create(fieldname=pythonname,filedname=pythonname)

# fetch all data from models (without anu condition)

var = models.objects.all()

# fetch all data from model but condition wise 

filter() : returns queryset

var = models.objects.filter(fieldname = value)


"""
def home(request):
    if 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role=="chairman":

            cid = Chairman.objects.get(user_id = uid)
            context = {
                        'uid' : uid,
                        'cid' : cid,
                    }
            return render(request,"chairmanapp/index.html",context)
        else:
            sid = Societymember.objects.get(user_id = uid)
            context = {
                        'uid' : uid,
                        'sid' : sid,
                    }
            return render(request,"societymemberapp/index.html",context)

    else:
        return redirect("login")


def login(request):
    if 'email' in request.session:
        return redirect ('home')
    else:
        if request.POST:
            pemail = request.POST['email']
            ppassword = request.POST['password']
            print("----->email ",pemail)
            try:

                uid = User.objects.get(email = pemail)
                if uid.password == ppassword:
                    if uid.role == "chairman":
                        
                        cid = Chairman.objects.get(user_id = uid)

                        print("firstname",cid.firstname)
                        print("SIGN IN BUTTON PRESS ----->",uid)
                        print(uid.role)
                        print(uid.password)
                        request.session['email'] = uid.email

                        return redirect("home")
                    else:

                        print("SOCIETY MEMBER")
                    
                    if uid.role == "Societymember":
                        
                        sid = Societymember.objects.get(user_id = uid)

                        print("firstname",sid.firstname)
                        print("SIGN IN BUTTON PRESS ----->",uid)
                        print(uid.role)
                        print(uid.password)
                        request.session['email'] = uid.email

                        return redirect("home")
                    else:

                        print("SOCIETY MEMBER")
                    
                    

                else:
                    context ={
                        'emsg' : "Invalid password"
                    }
                    print("somthing went wrong")
                    return render(request,"chairmanapp/login.html",context)
            except:
                context ={
                        'emsg' : "Invalid Email address"
                    }
                print("somthing went wrong")
                return render(request,"chairmanapp/login.html",context)
        else:
          print("---> login page refresh")
          return render(request,"chairmanapp/login.html")
def login_backend(request):
    if request.POST:
       
        uid = User.objects.get(pemail=request.session['email'])
        if uid is not None:
            login(request, uid)
            request.session.set_expiry(10)
            return redirect("login")
        else:
            return redirect("login_backend")
    else:
        return render(request,"chairmanapp/login.html")
        
def logout(request):
    if"email" in request.session:
        del request.session['email']  
        return redirect('login') 
    else:
        return redirect('login')        

def chairman_profile(request):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])
        cid = Chairman.objects.get(user_id = uid )
        if request.POST:
            firstname= request.POST['firstname']
            lastname= request.POST['lastname']

            cid.firstname = firstname
            cid.lastname = lastname
            if 'pictures' in request.FILES:
             cid.pic = request.FILES['picture']
            
             cid.save()
            
            context ={
                'uid': uid,
                'cid': cid,
            }
            return render(request,"chairmanapp/profile.html",context)
        else:
            context ={
                'uid': uid,
                'cid': cid,
            }
            return render(request,"chairmanapp/profile.html",context)
    else:
        return redirect("login")
    

def chairman_change_password(request):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])
        cid = Chairman.objects.get(user_id = uid )
        if request.POST:
            currentpassword = request.POST['currentpassword']
            newpassword = request.POST['newpassword']
            
            if uid.password == currentpassword:
                uid.password = newpassword
                uid.save()
                return redirect ("logout")
            else:
                pass
                
                context ={
                    'uid': uid,
                    'cid': cid,
                }
                return render(request,"chairmanapp/profile.html",context)
    else:
        
        context ={
                    'uid': uid,
                    'cid': cid,
        }
        return render(request,"chairmanapp/profile.html",context)

        
def add_member (request):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])
        cid = Chairman.objects.get(user_id = uid )
        if request.POST:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            House_no = request.POST['Houseno']
            contactno = request.POST['contactno']
            
            l1 = ['abc123','def456','hij789','klm011','opq1213']
            password = email[4:7]+contactno[3:7]+choice(l1)

            uid = User.objects.create(email = email,password = password, role = "societymember")
            sid = Societymember.objects.create(user_id = uid, firstname = firstname, lastname = lastname, contact_no = contactno, House_no = House_no)

            if sid:
                send_mail("Digital Society Password", "Your Password is : "+str(password),"shreehelly@gmail.com",[email])
                msg = "successfully societymember created !! plz check gmail account for password."
                context = {
                    'uid': uid,
                    'sid': sid,
                    'msg' : msg,
                }
                return render (request,"chairmanapp/add-member.html",context)
        else:
            context ={
                        'uid': uid,
                        'cid': cid,
                }
        return render(request,"chairmanapp/add-member.html",context)
    else:
        return render("login")
    
def all_member(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        cid = Chairman.objects.get(user_id = uid)

        sall = Societymember.objects.all()
        context = {
                    'uid' : uid,
                    'cid' : cid,
                    'sall' : sall,
                }
        return render(request,"chairmanapp/all-member.html",context) 

def add_notice(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid )

        if request.POST:
            
            nid = Notice.objects.create(
                user_id = uid,
                title = request.POST['title'],
                description = request.POST['description'],
            )
            nall = Notice.objects.all()
            context ={
                        'uid': uid,
                        'cid': cid,
                        'nall' : nall,
            }
            return render(request,"chairmanapp/notice-list.html",context)

        else:

            context ={
                        'uid': uid,
                        'cid': cid,
                    }
            return render(request,"chairmanapp/add-notice.html",context)
    else: 
        return redirect("login")   
    
def view_notice(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid )
        nall = Notice.objects.all()
        context ={
                        'uid': uid,
                        'cid': cid,
                        'nall' : nall,
                    }
        return render(request,"chairmanapp/notice-list.html",context)
    
def notice_details(request,pk):
    if "email" in request.session:
        print("-------> PK",pk)
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid )
        notice = Notice.objects.filter(id = pk)
        context ={
                        'uid': uid,
                        'cid': cid,
                        'notice' : notice,
                    }
        return render(request,"chairmanapp/notice-details.html",context)

def societyspecification_profile(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        sid = Societymember.objects.get(id = pk)
        context = {
                    'uid' : uid,
                    'cid' : cid,
                    'sid' : sid,
                }
        return render(request,"chairmanapp/specific-profile.html",context) 
    
def add_event(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        if request.POST:
            eid = Event.objects.create(
                 user_id = uid,
                 title = request.POST['title'],
                 description = request.POST['description']

            )
            eall = Event.objects.all()
            context = {
                    'uid' : uid,
                    'cid' : cid,
                    'eall' : eall,
                }
            return render(request,"chairmanapp/event-list.html",context)
        else:
            context = {
                        'uid' : uid,
                        'cid' : cid,
                    }
            return render(request,"chairmanapp/add-event.html",context)
    else:
        return redirect("login")
    
def view_event(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        eall = Event.objects.all()
        context = {
                    'uid' : uid,
                    'cid' : cid,
                    'eall' : eall,
                }
        return render(request,"chairmanapp/event-list.html",context)
    else:
        return redirect("login")
    
def view_event_details(request,pk):
    if "email" in request.session:
        print("----------------------->PK",pk)
        uid = User.objects.get(email=request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        event = Event.objects.filter(id = pk)
        context = {
                    'uid' : uid,
                    'cid' : cid,
                    'event' : event,
                }
        return render(request,"chairmanapp/event-details.html",context)
    else:
        return redirect("login")   
    
def add_maintainance(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        if request.POST:
            title = request.POST['title']
            amount = request.POST['amount']
            duedate = request.POST['duedate']

            sall = Societymember.objects.all()
            for i in sall:
                sid = Societymember.objects.get(id = i.id)
                print("===================------------------>>",sid)
                mid = Maintainance.objects.create(user_id = uid,member_id = sid,title=title,amount=amount,duedate=duedate)
                #send_mail("MAINTAINANCE : ",mid.title,"shreehelly@gmail.com",[i.member_id.user_id.email])
                status = "successfully Added..."
        context = {
            'uid' : uid,
            'cid' : cid,
            'status' : status,
            
        }
        return render(request,"chairmanapp/add-maintainance.html",context) 
    context = { 
                'uid' : uid,
                'cid' : cid,
            }
    return render(request,"chairmanapp/add-maintainance.html",context) 

def all_maintainance(request):   
     if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        cid = Chairman.objects.get(user_id = uid)

        mall = Maintainance.objects.all()
        total = 0
        for i in mall:
            total+= int(i.amount)
        context = { 
                'uid' : uid,
                'cid' : cid,
                'mall' : mall,
                'total' : total,
            }
        return render(request,"chairmanapp/all-maintainance.html",context)

# def add_complain(request):
#     if "email" in request.session:
#         uid = User.objects.get(email=request.session['email'])
#         cid = Chairman.objects.get(user_id = uid)
#         if request.POST:
#             nid = Complain.objects.create(
#                  user_id = uid,
#                  title = request.POST['title'],
#                  description = request.POST['description']

#             )
#             nall = Complain.objects.all()
#             context = {
#                     'uid' : uid,
#                     'cid' : cid,
#                     'nall' : nall,
#                 }
#             return render(request,"chairmanapp/complain-list.html",context)
#         else:
#             context = {
#                         'uid' : uid,
#                         'cid' : cid,
#                     }
#             return render(request,"chairmanapp/add-complain.html",context)
#     else:
#         return redirect("login")
    

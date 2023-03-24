from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from chairmanapp.models import *

# Create your views here.

# def home(request):
#     if 'email' in request.session:
#         uid = User.objects.get(email = request.session['email'])
#         if uid.role=="chairman":

#             sid = Societymember.objects.get(user_id = uid)
#             context = {
#                         'uid' : uid,
#                         'sid' : sid,
#                     }
#             return render(request,"chairmanapp/index.html",context)
#         else:
#             sid = Societymember.objects.get(user_id = uid)
#             context = {
#                         'uid' : uid,
#                         'sid' : sid,
#                     }
#             return render(request,"chairmanapp/index.html",context)

#     else:
#         return redirect("login")
    

def societymember_profile(request):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])
        sid = Societymember.objects.get(user_id = uid )
        if request.POST:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            city = request.POST['city']
            contact_no = request.POST['contact_no']
            House_no = request.POST['House_no']
            House_Owner = request.POST['House_Owner ']
            occupation = request.POST['occupation']
            Family_members = request.POST['Family_members']
            blood_group = request.POST['blood_group']

            sid.firstname = firstname
            sid.lastname = lastname
            sid.city = city
            sid.contact_no = contact_no
            sid.House_no = House_no
            sid.House_Owner = House_Owner
            sid.occupation = occupation
            sid.Family_members = Family_members
            sid.blood_group = blood_group
            
            if "picture" in request.FILES:
                sid.pic = request.FILES['picture']

            sid.save()

            contex = {
                        'uid' : uid,
                        'sid' : sid,
                    }
            return render(request,"societymemberapp/profile.html",contex)
        else:
            context ={
                'uid': uid,
                'sid': sid,
            }
        return render(request,"societymemberapp/profile.html",context)
    else:
        return redirect("login")
    
def societymember_change_password(request):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])
        sid = Societymember.objects.get(user_id = uid )
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
                    'sid': sid,
                }
                return render(request,"societymemberapp/profile.html",context)
    else:
        
        context ={
                    'uid': uid,
                    'sid': sid,
                }
        return render(request,"societymemberapp/profile.html",context)
   
def view_notice_society(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Societymember.objects.get(user_id = uid )
        nall = Notice.objects.all()
        context ={
                        'uid': uid,
                        'sid': sid,
                        'nall' : nall,
                    }
        return render(request,"societymemberapp/notice-list.html",context)
    
def notice_society_details(request,pk):
    if "email" in request.session:
        print("-------> PK",pk)
        uid = User.objects.get(email = request.session['email'])
        sid = Societymember.objects.get(user_id = uid )
        notice = Notice.objects.filter(id = pk)
        context ={
                        'uid': uid,
                        'sid': sid,
                        'notice' : notice,
                    }
        return render(request,"societymemberapp/notice_society_details.html",context)
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
# from django.contrib.auth.models import User,auth
from django.contrib import messages
from requests import session
from fileApp.models import *
from datetime import date
# Create your views here.

def login(req):

    if req.method == 'POST':
        email = req.POST['email']
        psw = req.POST['pass']

        try:
            user = employee.objects.get(emp_email=email)
            if user.emp_pass == psw:
                req.session['uID'] = user.id
                req.session['uName'] = user.first_name
                return redirect('')
            else:
                messages.error(req,'Invalid Credentials')

        except:
            messages.error(req,'No such user found')
            

        
    return render(req,'login.html')

def logout(req):

    if 'uID' in req.session.keys():
        del req.session['uID']
        del req.session['uName']
        return redirect('login')
    else:
        return redirect('login')


def home(req):
    if 'uID' in req.session.keys():
        list_file=[]
        user = employee.objects.get(id=req.session['uID'])
        filesD = fileDetail.objects.filter(given_to=user)
        for i in filesD:
            list_file.append(i.file_to)
        return render(req,'home.html',{'files':list_file,'u':user})
    else:
        return redirect('login')



def viewFile(req,file_id):
    if 'uID' in req.session.keys():
        file1 = file.objects.get(id=file_id)
        user = getuser(req)
        return render(req,'file.html',{'file':file1,'u':user})
    else:
        return redirect('login')


def approve(req,f_id):
    if 'uID' in req.session.keys():
        user = employee.objects.get(id=req.session['uID'])
        file1 = file.objects.get(id=f_id)
        if user == file1.upload_by:
            messages.success(req,'You can`t approve your own file')
            return redirect(req.META.get('HTTP_REFERER'))
        d_file = fileDetail.objects.get(file_to=file1)
        d_file.approved_by.add(user)
        d_file.given_to.remove(user)
        messages.success(req,' Document Approved')
        return redirect("")


    else:
        return redirect('login')


def reject(req,fl_id):
    if 'uID' in req.session.keys():
        user = employee.objects.get(id=req.session['uID'])
        file1 = file.objects.get(id=fl_id)
        if user == file1.upload_by:
            messages.success(req,'You can`t reject your own file')
            return redirect(req.META.get('HTTP_REFERER'))
        d_file = fileDetail.objects.get(file_to=file1)
        d_file.rejected_by.add(user)
        d_file.given_to.remove(user)
        messages.success(req,' Document Rejected')
        return redirect("")

        
    else:
        return redirect('login')

def addfile(req):
    if 'uID' in req.session.keys():

        if req.method == 'POST':
            model = file()
            model.name = req.POST['fname']
            model.desc = req.POST['fdesc']
            model.file = req.FILES.get('file_path')
            model.upload_at = date.today()

            user = getuser(req)
            model.upload_by = user
            model.save()

            messages.success(req,'File successfully added')
        user = getuser(req)
        return render(req,'addfile.html',{'u':user})
    else:
        return redirect('login')



def yourfiles(req):
    if 'uID' in req.session.keys():
        
        user = getuser(req)
        files = file.objects.filter(upload_by=user)
        return render(req,'yourfile.html',{'files':files,'u':user})
    else:
        return redirect('login')


def delete(req,did):
    if 'uID' in req.session.keys():
        file.objects.get(id=did).delete()
        messages.success(req,'File Deleted successfully')
        return redirect('yourfiles')
    else:
        return redirect('login')


def allocate(req,fid):
    if 'uID' in req.session.keys():
        f_file = file.objects.get(id=fid)
        if req.method == 'POST':
            list_o = []
            list_1 = []
            list_u = req.POST.getlist('check')
            for i in list_u:
                u = employee.objects.get(id=int(i))
                list_o.append(u)
            # print(list_o)
            try:
                a_file = fileDetail.objects.get(file_to = f_file)
                alredy_add = a_file.given_to.all()
                for j in alredy_add:
                    list_o.append(j)
            except:
                a_file = None

            if a_file is not None:
                a_file.given_to.set(list_o)
            else:
                model = fileDetail()
                model.file_to = file.objects.get(id=fid)
                model.save()
                model.given_to.set(list_o)

        users = employee.objects.exclude(id=req.session['uID'])
        u = getuser(req)
        return render(req,'allocate.html',{'users':users,'i':f_file,'u':u})
    else:
        return redirect('login')


def detail(req,data):
    if 'uID' in req.session.keys():
        D_file = file.objects.get(id=data)
        try:
            df = fileDetail.objects.get(file_to=D_file)
        except:
            messages.success(req,'File Not yet allocated')
            return redirect('yourfiles')
        Approv = df.approved_by.all()
        reject = df.rejected_by.all()
        user = getuser(req)
        return render(req,'detail.html',{'i':D_file,'apr_us':Approv,'rjc_us':reject,'u':user})
    else:
        return redirect('login')



def profile(req):
    if 'uID' in req.session.keys():
        if req.method == 'POST':
            f_name = req.POST['f_name'] 
            l_name = req.POST['l_name'] 
            email = req.POST['email'] 
            phone = req.POST['phone'] 
            add = req.POST['add']
            date = req.POST['dob']
            profile = req.FILES.get('profile')
            psw = req.POST['pass'] 
            if req.POST['pass'] == req.POST['repass']:
                us = employee.objects.get(id=req.session['uID'])
                us.first_name = f_name
                us.last_name = l_name
                us.emp_email = email
                us.phone = phone
                us.img = profile
                us.dob = date
                us.emp_pass = psw
                us.save()
# .update(first_name=f_name,last_name=l_name,emp_email=email,phone=phone,dob=date,emp_pass=psw)

            else:
                pass
        u = employee.objects.get(id=req.session['uID'])
        return render(req,'profile.html',{'user':u})
    else:
        return redirect('login')

def regs(req):
    return render(req,'regs.html')

# def home(req):
#     if 'uID' in req.session.keys():
#         return render(req,'home.html')
#     else:
#         return redirect('login')

# -------------------------------------Test purpose
# def test(req):
#     if 'uID' in req.session.keys():
#         if req.method == 'POST':
        
#             list_u = req.POST.getlist('test')
#             print(list_u)
#             # print(list_u['checkbox'])
#             # for i in list_u:
            
#         return render(req,'test.html')
#     else:
#         return redirect('login')
def getuser(req):
    user = employee.objects.get(id=req.session['uID'])
    return user
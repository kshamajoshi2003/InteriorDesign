from django.shortcuts import render,redirect
from interior_app.models import UserRegistration,AddPayment,UploadDesigns,GiveFeedback,UserLogin,AddEmployee,AddBooking
from django.core.files.storage import FileSystemStorage
from interior.settings import BASE_DIR
import os
import random
import smtplib
import datetime
from django.contrib import messages


def index(request):
    return render(request,'index.html')


def user_home(request):
    return render(request,'user_home.html')

def admin_home(request):
    return render(request,'admin_home.html')

def worker_home(request):
    return render(request,'worker_home.html')

def login(request):
    if request.method=="POST":
        username=request.POST.get('t1')
        request.session['username']=username
        password=request.POST.get('t2')
        print(password)
        request.session['username']=username
        ucheck=UserLogin.objects.filter(username=username).count()
        if ucheck>=1:
            udata=UserLogin.objects.get(username=username)
            upass=udata.password
            print("Hello",upass)
            utype=udata.utype
            if (upass==password):

                if utype=="admin":
                    return redirect('admin_home')

                if utype=="user":
                    return redirect('user_home')

                if utype=="worker":
                    return redirect('worker_home')

            else:
                return render(request,'login.html',{'msg':'invalid password'})
        else:
            return render(request, 'login.html', {'msg': 'invalid username'})

    return render(request, 'login.html')


def reg(request):
    if request.method=="POST":
        fname=request.POST.get('t1')
        lname = request.POST.get('t2')
        gender = request.POST.get('t3')
        address = request.POST.get('t4')
        pincode = request.POST.get('t5')
        email = request.POST.get('t6')
        mobile_no = request.POST.get('t7')
        password = request.POST.get('t8')
        UserRegistration.objects.create(fname=fname,lname=lname,gender=gender,address=address,pincode=pincode,email=email,mobile_no=mobile_no)
        UserLogin.objects.create(username=email,password=password,utype='user')
        return render(request,'reg.html',{'msg':'Registered Successfully'})

    return render(request,'reg.html')


def add_workers(request):
    if request.method=="POST" and request.FILES['file']:
        emp_name = request.POST.get('t2')
        yoj = request.POST.get('t3')
        experience = request.POST.get('t4')
        mobile_no = request.POST.get('t5')
        address = request.POST.get('t6')
        email = request.POST.get('t7')
        profile=request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(profile.name, profile)
        fileurl = fs.url(filename)
        AddEmployee.objects.create(emp_name=emp_name,yoj=yoj,experience=experience,mobile_no=mobile_no,address=address,email=email,profile=profile)
        UserLogin.objects.create(username=email,password=mobile_no,utype='worker')
        return render(request,'add_workers.html',{'msg':'Added Successfully'})

    return render(request,'add_workers.html')


def upload_design(request):
    username=request.session['username']
    data=AddEmployee.objects.get(email=username)
    if request.method=="POST" and request.FILES['file']:
        service=request.POST.get('service')
        design_photo=request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(design_photo.name,design_photo)
        upload_file_url = fs.url(filename)
        pat = os.path.join(BASE_DIR, '/media/' + filename)
        UploadDesigns.objects.create(user_id=username,design_photo=design_photo,service_type=service)
        return render(request,'upload_design.html',{'msg':'Uploaded Successfully'})
    return render(request,'upload_design.html')

def view_workers(request):
    userdict=AddEmployee.objects.all()
    return render(request,'view_workers.html',{'userdict':userdict})


def booking_requests(request):
    userdict = AddBooking.objects.all()
    return render(request,'booking_requests.html',{'userdict':userdict})


def send_service_request(request):
    userdict=AddEmployee.objects.all()
    return render(request,'send_service_request.html',{'userdict':userdict})


def send_service_request_next(request,cat):
    request.session['cat']=cat
    userdict=UploadDesigns.objects.filter(user_id=cat).values()
    if request.method=="POST":
        user_id = request.session['username']
        provider_id = request.session['cat']
        n = datetime.datetime.now()
        book_date = n.strftime("%Y-%m-%d")
        if request.POST.get('service'):
            service = request.POST.get('service')
            service = str(service)
            s=service[-1]
            s1=s.split(',')
            AddBooking.objects.create(user_id=user_id, service=service, status='pending', book_date=book_date,
                                      provider_id=provider_id)
            messages.info(request, 'Thank you for Booking!')
            return redirect('send_service_request')
        else:
            messages.info(request, 'Please Select Service you want!')
            return redirect('send_service_request')

    return render(request,'send_service_request_next.html',{'userdict':userdict})


def send_booking_request(request):
    user_id=request.session['username']
    provider_id=request.session['cat']
    n=datetime.datetime.now()
    book_date=n.strftime("%Y-%m-%d")
    if request.method=="POST":
        if request.POST.get('service'):
            service = request.POST.get('service')
            service=str(service)
            l=len(service)
            vii=service[0:1-1]
            present=vii.split(",")
            print(present)
            #li=[]
            AddBooking.objects.create(user_id=user_id,service=service,status='pending',book_date=book_date,provider_id=provider_id)
            messages.info(request,'Thank you for Booking!')
            return redirect('send_service_request')
        else:
            return render(request,'send_booking_request.html')
    return render(request,'send_booking_request.html')

def request_status_user(request):
    uid=request.session['username']
    userdict=AddBooking.objects.filter(user_id=uid).values()
    return render(request,'request_status_user.html',{'userdict':userdict})

def remove_booking(request,pk):
    udata=AddBooking.objects.get(id=pk)
    udata.delete()
    return redirect('request_status_user')

def worker_del(request,pk):
    udata=AddEmployee.objects.get(id=pk)
    udata.delete()
    return redirect('view_workers')

def design_del(request,pk):
    udata=UploadDesigns.objects.get(id=pk)
    udata.delete()
    return redirect('view_upload_design')

def worker_edit(request,pk):
    udata=AddEmployee.objects.filter(id=pk)
    if request.method=="POST":
        emp_name = request.POST.get('t2')
        yoj = request.POST.get('t3')
        experience = request.POST.get('t4')
        mobile_no = request.POST.get('t5')
        address = request.POST.get('t6')
        email = request.POST.get('t7')
        if (len(request.FILES) != 0):
            profile = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(profile.name, profile)
            fileurl = fs.url(filename)
            AddEmployee.objects.filter(id=pk).update(emp_name=emp_name, yoj=yoj, experience=experience, mobile_no=mobile_no,address=address,email=email,profile=profile)
            return redirect('view_workers')
        else:
            AddEmployee.objects.filter(id=pk).update(emp_name=emp_name, yoj=yoj, experience=experience,mobile_no=mobile_no,address=address,email=email)
            return redirect('view_workers')

    return render(request,'worker_edit.html',{'udata':udata})


def design_edit(request,pk):
    udata=UploadDesigns.objects.filter(id=pk).values()
    if request.method=="POST":
        service = request.POST.get('service')
        if (len(request.FILES) != 0):
            design_photo = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(design_photo.name, design_photo)
            upload_file_url = fs.url(filename)
            pat = os.path.join(BASE_DIR, '/media/' + filename)
            UploadDesigns.objects.filter(id=pk).update(design_photo=design_photo, service_type=service)
            return redirect('view_upload_design')
        else:
            UploadDesigns.objects.filter(id=pk).update(service_type=service)
            return redirect('view_upload_design')
    return render(request,'design_edit.html',{'udata':udata})


def view_upload_design(request):
    uid=request.session['username']
    udata=UploadDesigns.objects.filter(user_id=uid).values()
    return render(request,'view_upload_design.html',{'udata':udata})


def give_feedback(request):
    username=request.session['username']
    if request.method=="POST":
        service=request.POST.get('t1')
        comments=request.POST.get('t2')
        GiveFeedback.objects.create(user_id=username,service=service,comments=comments)
        return render(request, 'give_feedback.html',{'msg':'Thank you for your feedback'})
    return render(request,'give_feedback.html')

def view_booking_requests(request):
    uid=request.session['username']
    userdict=AddBooking.objects.filter(provider_id=uid).values()
    return render(request,'view_booking_requests.html',{'userdict':userdict})

def update_booking_status(request,pk):
    if request.method=="POST":
        status=request.POST.get('t1')
        cost = request.POST.get('t2')
        AddBooking.objects.filter(id=pk).update(status=status,cost=cost)
        return redirect('view_booking_requests')
    return render(request,'update_booking_status.html')


def view_feedback_worker(request):
    userdict=GiveFeedback.objects.all()
    return render(request,'view_feedback_worker.html',{'userdict':userdict})

def view_user(request,email):
    udata=UserRegistration.objects.filter(email=email).values()
    return render(request,'view_user.html',{'udata':udata})


def pay(request,pk):
    uid=request.session['username']
    udata=AddBooking.objects.get(id=pk)
    cost=udata.cost
    provider_id=udata.provider_id
    n=datetime.datetime.now()
    paid_date=n.strftime("%Y-%m-%d")
    if request.method=="POST":
        AddPayment.objects.create(user_id=uid,book_id=pk,amount=cost,paid_date=paid_date,provider_id=provider_id)
        AddBooking.objects.filter(id=pk).update(payment_status='Paid')
        return render(request, 'pay.html', {'msg': 'Payment has been done successfully'})
    return render(request,'pay.html',{'amount':cost})


def payment_report(request):
    uid=request.session['username']
    udata=AddPayment.objects.filter(provider_id=uid).values()
    return render(request,'payment_report.html',{'udata':udata})
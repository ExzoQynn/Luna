from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import os

# Create your views here.
def HomePage(request):
    # return HttpResponse("Hello World !!")
    return render(request,'site/home.html')

def SignInPage(request):
    return render(request,'site/sign_in.html')

def SignUpPage(request):
    return render(request,'site/sign_up.html')

def Register(request):
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    repassword = request.POST['repassword'] 

    if password == repassword :
        if User.objects.filter( username = username).exists():
            messages.warning(request,'Username มีคนใช้แล้ว')
            return redirect('/SignUp')
        elif User.objects.filter( email = email ).exists():
            messages.warning(request,'Email นี้เคยลงทะเบียนแล้ว')
            return redirect('/SignUp')
        else :
            user = User.objects.create_user(
                email = email,
                username = username,
                password = password,
            )

            set_profile = Profile()
            set_profile.user = user
            set_profile.save()
            user.save()
            return redirect('/SignIn')
    else :
        messages.warning(request,'รหัสผ่านไม่ตรงกัน')
        return redirect('/SignUp')

def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    
    #check user , password 
    user = auth.authenticate(
        username = username,
        password = password
    )

    if user is not None : 
        auth.login(request,user)
        return redirect('/')
    else :
        messages.warning(request,'ไม่พบข้อมูล')
        return redirect('/SignIn')

def SingOut(request):
    auth.logout(request)
    return redirect('/')

def DashBoard(request):
    return render(request,'site/dashboard.html')

@login_required
def ProfilePage(request):
    username = request.user.username
    edit_profile = User.objects.get(username=username)

    if request.method == 'POST':
        data = request.POST.copy()
        email = data.get('email')
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        try :
            set_profile = Profile.objects.get(user=edit_profile)
            os.remove('media/'+set_profile.photo_profile.name)
        except:
            set_profile = Profile()
            set_profile.user = edit_profile

        ###### File system #######    
        fs = FileSystemStorage()
        file_image = request.FILES['photo_profile']
        file_image_name = file_image.name
        file_name = fs.save('photo_profile/'+file_image_name,file_image)
        upload_file_url = fs.url(file_name)
        set_profile.photo_profile = upload_file_url[7:]
        set_profile.save()   
        ###### File system #######    
        
        
        edit_profile.username = username
        edit_profile.email = email
        edit_profile.first_name = first_name
        edit_profile.last_name = last_name

        edit_profile.save()
        return redirect('/Profile')
    
    context = {'data' : edit_profile}
    return render(request,'site/profile.html',context)


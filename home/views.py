from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout



# Create your views here.
def home(request):
    return render(request,'home/home.html')

def contact(request):
    messages.success(request, 'welcome to contact')
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['desc']
        if len(name)<2 or len(email)<4 or len(phone)<10 or len(content)<4 :
            messages.error(request,'please enter correctly')
        else:
            contact = Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,'your message has been successfully sent....')
    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPost = Post.objects.none()
    else:
        allPostTitle = Post.objects.filter(title__icontains=query)
        allPostContent = Post.objects.filter(content__icontains=query)
        allPost = allPostTitle.union(allPostContent)
    if allPost.count() == 0:
            messages.error(request,'please enter correctly')
    params = {'allPost':allPost,'query':query}
    return render(request,'home/search.html',params)

def handleSignup(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['passwd1']
        password2 = request.POST['passwd2']
        #check
        if len(username) >10:
            messages.error(request,'username must be 10 character')
            return redirect('/')
        
        if username.isalnum :
            messages.error(request,'username should be alphanumeric')
            return redirect('/')

        if password1 != password2:
            messages.error(request,"password doesn't match")
            return redirect('/')

        # create user
        myuser = User.objects.create_user(username,email,password1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request,'your iCoder account has been successfully.!!')
        return redirect('/')
    else:
        return HttpResponse("404-Not Found")

def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        passwd = request.POST['passwd']

        user =authenticate(username=loginusername,password=passwd)

        if user is not None:
            login(request,user)
            messages.success(request,'successfully logged In !!')
            return redirect('/')
        else:
            messages.error(request,'Invalid credantial, please try again .')
            return redirect('/')
            
    return HttpResponse("404-not found")
    
def handleLogout(request):
    logout(request)
    messages.success(request,'successfully logged out !!')
    return redirect('/')
    return HttpResponse("404-not found")
    
    
    
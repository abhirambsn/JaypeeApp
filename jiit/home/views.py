from atexit import register
from sre_constants import SUCCESS
from django.http import HttpResponse
from django.shortcuts import render
from requests import session
import pyrebase
 
configuration={
    "apiKey": "AIzaSyA3hLk3kakqgjmLh8KUWDSvQ_dF1FBmhhg",
    "authDomain": "jiit-cdf9e.firebaseapp.com",
    "databaseURL": "https://jiit-cdf9e-default-rtdb.firebaseio.com",
    "projectId": "jiit-cdf9e",
    "storageBucket": "jiit-cdf9e.appspot.com",
    "messagingSenderId": "136044027072",
    "appId": "1:136044027072:web:3f93252f18832acd00a125",
    "measurementId": "G-SH43C5V7ZS"
}
firebase=pyrebase.initialize_app(configuration)
authe = firebase.auth()
db=firebase.database()

def index(request):
    context = {}

    if "email" in request.session:
        context["loggedIn"] = True
    else:
        context["loggedIn"] = False

    return render(request, "home/index.html", context)


def login(request):

    context = {}
    if "email" in request.session:
        context["loggedIn"] = True
    else:
        context["loggedIn"] = False

    if "email" in request.session:
        context["email"] = request.session['email']
        return render(request, "home/success.html", context)

    return render(request, "home/login.html", context)

def loginCheck(request):
    if "email" in request.session:
        return render(request, "home/success.html", {"email": request.session['email']})

    email = request.POST['email']
    pwd = request.POST['pwd']
    try:
        user = authe.sign_in_with_email_and_password(email, pwd)
    except:
        context = {"message": "Failed"}
        return render(request, "home/login.html", context)
    
    request.session['userId'] = user['localId']
    request.session['email'] = email
    return render(request, "home/success.html", {"email": email, "loggedIn": True})

def logout(request):
    try:
        del request.session['email']
    except:
        pass
    return render(request,"home/login.html", {"message": "Logged Out!"})

def signUp(request):
    context = {}
    if "email" in request.session:
        context["loggedIn"] = True
    else:
        context["loggedIn"] = False

    if "email" in request.session:
        context["email"] = request.session['email']
        return render(request, "home/success.html", context)

    return render(request, "home/register.html")

def signUpCheck(request):

    context = {}
    if "email" in request.session:
        context["loggedIn"] = True
    else:
        context["loggedIn"] = False

    if "email" in request.session:
        context["email"] = request.session['email']
        return render(request, "home/success.html", context)

    if request.method != "POST":
        return HttpResponse('No user data submitted!')

    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    pwd = request.POST.get('pwd')
    try:
        user=authe.create_user_with_email_and_password(str(email), str(pwd))
    except:
        return render(request, "home/register.html", {"message": "Failed registration!"})
    
    db.child('register').child(user['localId']).child('basicDetails')
    data = {
            'first-name': fname,
            'last-name': lname,
            'phone': phone
            }
    if db.set(data):
        return render(request,"home/login.html", {"message": "Registered successfully!"})

    return render(request, "home/register.html", {"message": "Failed basic details!"})

    
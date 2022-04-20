from django.shortcuts import render
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



def registrar(request):
    if "userId" in request.session:
        data = db.child('register').get().val()
        return render(request, "registrar/login.html", {"loggedIn": True, "data": data.items()})
    
    return render(request, "registrar/registrar.html", {"message": False})

def registrarLogin(request):
    if "userId" in request.session:
        data = db.child('register').get().val()
        data = data.values()
        return render(request, "registrar/login.html", {"loggedIn": True, "data": list(data)})

    if request.method == "POST":
        email = request.POST['email']
        pwd = request.POST['pwd']
        try:
            user = authe.sign_in_with_email_and_password(email, pwd)
        except:
            context = {"message": "Failed"}
            return render(request, "registrar/registrar.html", context)
        
        request.session['userId'] = user['localId']
        data = db.child('register').get().val()
        data = data.values()
        return render(request, "registrar/login.html", {"loggedIn": True, "data": data})

def registrarLogout(request):
    try:
        del request.session['userId']
    except:
        pass
    return render(request, "registrar/registrar.html", {"message": "Logged Out!"})

# admin@jiit.com
# admin1234
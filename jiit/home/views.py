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

def index(request):
    last_record = db.child('register').order_by_key().limit_to_last(1).get().val()
    lr = str(list(last_record.keys())[0])
    if not db.child('register').shallow().get().val():
        data = {"fname": "user doesn't exist"}
    else:
        data = {
            "fname": db.child('register').child(lr).child('first-name').get().val(),
            "lname": db.child('register').child(lr).child('last-name').get().val(),
            "email": db.child('register').child(lr).child('email').get().val(),
            "phone": db.child('register').child(lr).child('phone').get().val(),
            "password": db.child('register').child(lr).child('password').get().val()
        }

    return render(request, "home/index.html", data)

def form(request):
    last_record = db.child('register').order_by_key().limit_to_last(1).get().val()
    context = {"lastRecord": str(list(last_record.keys())[0])}
    return render(request, "home/form.html", context)

def formDatabase(request):
    lastRecord = request.POST.get('lastRecord', False)
    fname = request.POST.get('fname', False)
    lname = request.POST.get('lname', False)
    email = request.POST.get('email', False)
    phone = request.POST.get('phone', False)
    pwd = request.POST.get('pwd', False)
    nextUser = int(lastRecord.split("user-", 1)[1])+1
    newRecord = "user-"+str(nextUser)
    db.child('register').child(newRecord)
    data = {
        "first-name": fname, 
        "last-name": lname,
        "email": email,
        "phone": phone, 
        "password": pwd
    }
    if db.set(data):
        return render(request, "home/form.html", {"message": "success"})
    
    return render(request, "home/form.html", {"message": "failed"})

def login(request):
    return render(request, "home/login.html")

def loginCheck(request):
    email = request.POST['email']
    pwd = request.POST['pwd']
    users = list(db.child('register').get().val().keys())
    for user in users:
        if email == db.child('register').child(user).child('email').get().val() and pwd == db.child('register').child(user).child('password').get().val():
            context = {
                "message": "Success"
            }
        else:
            context = {
                "message": "Failed"
            }
    return render(request, "home/login.html", context)
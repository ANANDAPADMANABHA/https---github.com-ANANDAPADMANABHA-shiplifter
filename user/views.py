from itertools import product
import random
import re
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from django.shortcuts import redirect, render
from orders.models import Orders
from theproducts.models import Product
from accounts.models import *
from cartapp.models import *
from twilio.rest import Client
from django.contrib import auth
from cartapp.views import _cart_id, checkout 




# Create your views here.

def home(request):
    user = request.user

    acc= Account.objects.all()
    values = Product.objects.all()
    return render(request,'index.html',{'values':values,'acc':acc})

def signin(request):
    return render(request,'signinuser.html')

def userlogout(request):
    logout(request)
    return redirect(home)




def userSignup(request):
    if request.method == "POST":
        username    = request.POST['username']
        first_name  = request.POST['first_name']
        last_name   = request.POST['last_name']
        email       = request.POST['email']
        password1   = request.POST['password1']
        password2   = request.POST['password2']
        phone_number    = request.POST['phone_number']
        
        print (email)
        if password1 == password2 :
            username_pattern = "^[A-Za-z\s]{3,}$"
            username_verify = re.match(username_pattern,username)

            if username == "" and email == "" and password1 == "" and password2 == "":
                messages.error(request,'Username must not be empty',extra_tags='signupusername')
                messages.error(request,"Email must not be empty", extra_tags='signupemail')
                messages.error(request,"password must not be empty", extra_tags='signuppassword')
                return redirect(userSignup)

            else:

                if username_verify is None:
                    messages.error(request,'Username must contain charecters only',extra_tags='signupusername')
                    return redirect(userSignup)
                if Account.objects.filter(username = username).exists():
                    print('GETTING INTO USERNAME')
                    messages.error(request, "Username already taken", extra_tags='signupusername')
                    return redirect(userSignup)
                if Account.objects.filter(email = email).exists():
                    print('GETTING INTO EMAIL')
                    messages.error(request,"Email already taken", extra_tags='signupemail')
                    return redirect(userSignup)
                else:
                    
                    user = Account.objects.create_user(username= username,first_name =first_name ,last_name=last_name,email = email,phone_number=phone_number, password = password1)
                    
                    user.save()
                    # user_name = user
                    # context = { 
                    #     'user_name':user_name
                    # }
                    return redirect(signin)

        else:
            messages.error(request,"Enter matching passwords", extra_tags='signuppassword')
            return render(request,'signupuser.html')
    
    else:
        return render(request,'signupuser.html')
            

def userSignin(request):
    
    if request.method == 'POST':
        username    = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username,password = password)
        if user is not None :
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                cart_item = CartItem.objects.filter(cart = cart)
                user_cart = CartItem.objects.filter(user = user)
                
                for x in cart_item:
                    a=0
                    for y in user_cart:
                        if x.product == y.product:
                            y.quantity += x.quantity 
                            y.save()
                            x.delete()
                            a=1
                            break
                    if a==0:
                        x.user=user
                        x.save()
            except:
                pass
                
            
            request.session['username']=username
            login(request,user)
            
            
            return redirect(home)

        else:
            messages.error(request,'invalid credentials')
            return redirect(userSignin)
    return render(request,'signinuser.html')

def otplogin(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        phone_no="+91" + phone_number
        if Account.objects.filter(phone_number=phone_number).exists():

                
           
                # Your Account SID twilio
                account_sid = 'AC9b76eab7cca4d234d3f201e91485225e'
                # Your Auth Token twilio
                auth_token  = '5fbd50179cb654cb2e93049701e20300'

                client = Client(account_sid, auth_token)

                global otp
                otp     =   str(random.randint(1000,9999))
                message      = client.messages.create(
                    to      ='+917306221165',
                    from_    ='+14422498718',
                    body    ='Your OTP code is'+ otp)

                messages.success(request,'OTP has been sent to 7306221165')
                return redirect(otpverify)

        else:
            messages.info(request,'invalid Mobile number')
            return redirect(otplogin)

    return render(request,'otpenter.html')

def otpverify(request):
    if request.method == 'POST':
        user      = Account.objects.get(phone_number=7306221165)
        otpvalue  = request.POST.get('otp')
        if otpvalue == otp:
            print('VALUE IS EQUAL')
            login(request, user)
            return redirect(home)
        else:
            messages.error(request, 'Invalid OTP')
            print('ERROR ERROR')
            return redirect(otplogin)
    return render(request,'otplogin.html')

def productDisplay(request,id):
    acc= Account.objects.all()
    thisProduct = Product.objects.get(id = id)
    return render(request,'productDetails.html',{'thisProduct':thisProduct,'acc':acc})


 
def userprofile(request):
    acc = Account.objects.get(email = request.user )
    print(acc)
    addresses = Address.objects.filter(user = request.user)
    print(addresses) 
    context = {
        'acc':acc,
        'addresses':addresses
    }
    return render(request,'userprofile.html',context)



def myorders(request):
    order = Orders.objects.filter(user = request.user ).order_by('id')
    
    context = {
       'order':order 
    }
    return render(request,'myorders.html',context)


    
def ordercancel(request,id):
    user = request.user
    order = Orders.objects.get(id = id ,user = user)

    order.status = 'Cancelled'
    order.save()

    return redirect(myorders)


def changepassword(request):
    
    if request.method == "POST":
        current_password = request.POST.get('currentpassword')
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirmpassword')

        
        acc = Account.objects.get(email = request.user)
        passw = acc.check_password(current_password)
        
        if new_password == confirm_password:
            if  passw:
                acc.set_password(new_password) 
                acc.save()
                messages.success(request,"password changed Succesfully !")

                return redirect(userSignin)
            else:
                messages.error(request,"password doesnt exist !")
                return redirect('changepassword')
            
    return render(request,'changepassword.html')
from ast import Try
from asyncio.windows_events import NULL
from calendar import c
import imp
from itertools import product
import random
import re
from unicodedata import name
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator ,EmptyPage, InvalidPage
from django.shortcuts import redirect, render
from orders.models import OrderProduct, Orders
from theproducts.models import Categoryies, Product
from accounts.models import *
from cartapp.models import *
from twilio.rest import Client
from django.contrib import auth
from cartapp.views import _cart_id, checkout
import user 
from myadmin.models import *



# Create your views here.

def home(request):
    user = request.user
    acc= Account.objects.all()
    cat = Categoryies.objects.get(category_name = 'limited deal')
    values1 = Product.objects.filter(category =cat )

    cat1 = Categoryies.objects.get(category_name = 'demand')
    values2 = Product.objects.filter(category =cat1 )

    cat2 = Categoryies.objects.get(category_name = 'Hot Trending Products')
    values3 = Product.objects.filter(category =cat2 )

    banner = Banner.objects.filter(is_selected = True)
    cat3 = Categoryies.objects.get(category_name = 'Laptops')

    hot = Product.objects.filter(category =cat2 )[0:4]
    onsale = Product.objects.filter(category =cat1 )[0:4]
    laps = Product.objects.filter(category =cat3 )[0:4]



    return render(request,'index.html',{'values':values1,'acc':acc ,'values2':values2,'values3':values3,'banner':banner,'hot':hot,'onsale':onsale,'laps':laps})


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

            if username == "" or email == "" or password1 == "" or password2 == "":
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
    acc= Account.objects.all().order_by('id')
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
    order = Orders.objects.filter(user = request.user ).order_by('-id')
    p = Paginator(order,9)
    page = request.GET.get('page')
    orders = p.get_page(page)


    context = {
       'orders':orders 
    }
    return render(request,'myorders.html',context)


    
def ordercancel(request,id):
    print('hahahahahahahahahahhahahahhahahaha')
    print(request.user)
    order = OrderProduct.objects.get(id = id )
    product = Product.objects.get(id =order.product.id)
    acc =Account.objects.get(email = request.user )

    if acc.wallet:

        acc.wallet += order.price
        
    else:
        acc.wallet = order.price
    acc.save()
    order.status = 'Cancelled'
    order.save()

    product.stock +=order.quantity
    product.save()

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
                login(request,acc)
                messages.success(request,"password changed Succesfully !")

                return redirect(userprofile)
            else:
                messages.error(request,"password doesnt exist !")
                return redirect('changepassword')
            
    return render(request,'changepassword.html')

def search(request):
    try:
        q = request.GET['search']

        data = Product.objects.all()
        datas = []
    
        for i in data :
            datas.append(i.name)

        print(datas)

        for i in datas:
           if q.lower() in i.lower():
               searched = Product.objects.filter(name = i)

        return render(request, 'base.html',{'data':searched})
    except:
        return render(request,'noproduct.html')

    


    # data = Product.objects.filter(name = q).order_by('id')
def homecart(request):
    if request.user.is_authenticate:
        cart = CartItem.objects.filter(user=request.user)

        return render (request,'base.html' , {'cart':cart})
    
def shoplaptop(request):
    cat = Categoryies.objects.get(category_name='Laptops')
    value = Product.objects.filter(category = cat)

    return render (request,'shop.html' ,{'values':value})
    
def shopphone(request):
    cat = Categoryies.objects.get(category_name='Smart Phones')
    value = Product.objects.filter(category = cat)

    return render (request,'shop.html' ,{'values':value})

def shopheadphone(request):
    cat = Categoryies.objects.get(category_name='Hot Trending Products')
    value = Product.objects.filter(category = cat)

    return render (request,'shop.html' ,{'values':value})

def shoptab(request):
    cat = Categoryies.objects.get(category_name='Tablets')
    value = Product.objects.filter(category = cat)

    return render (request,'shop.html' ,{'values':value})

def limiteddeal(request):
    cat = Categoryies.objects.get(category_name='limited deal')
    value = Product.objects.filter(category = cat)

    return render (request,'shop.html' ,{'values':value})

def demand(request):
    cat = Categoryies.objects.get(category_name='demand')
    value = Product.objects.filter(category = cat)

    return render (request,'shop.html' ,{'values':value})

def orderdetails(request,id):
    orderprod = OrderProduct.objects.filter(order = id).order_by('-id')
    
    return render (request,'orderdetails.html',{'orderprod':orderprod} )

    
def orderreturn(request,id):
    
    order = OrderProduct.objects.get(id = id )
    product = Product.objects.get(id =order.product.id)
    acc =Account.objects.get(username = request.user )
    
    acc.wallet = order.price
    acc.save()

    order.status = 'Returned'
    order.save()

    product.stock +=order.quantity
    product.save()

    return redirect(myorders)

def addressdelete(request,id):
    address = Address.objects.get(id = id)
    address.delete()
    return redirect(userprofile)

def editaddress(request,id):
    address = Address.objects.get(id = id)
    if request.method == "POST":
        firstname    = request.POST.get('firstname')
        lastname    = request.POST.get('lastname')
        housename    = request.POST.get('housename')
        locality    = request.POST.get('locality')
        city    = request.POST.get('city')
        state    = request.POST.get('state')
        pincode    = request.POST.get('pincode')
        phonenumber    = request.POST.get('phonenumber')
        

        address.firstname = firstname
        address.lastname = lastname
        address.housename = housename
        address.locality = locality
        address.city = city
        address.state = state
        address.pincode = pincode
        address.phonenumber = phonenumber
        address.save()

        return redirect(userprofile)

    return render (request,"editaddress.html",{'address':address})
    
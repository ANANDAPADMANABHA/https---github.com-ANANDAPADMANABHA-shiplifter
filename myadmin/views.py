from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

from accounts.models import Account
from orders.models import Orders
from theproducts.models import Product , Categoryies
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator ,EmptyPage, InvalidPage


# Create your views here.

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def adminLogin(request):
    if 'username' in request.session:
        return redirect(admin_home)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username = username,password=password)

        if user is not None:
            if user.is_superuser:
                request.session['username']=username
                login(request,user)
                return redirect(admin_home)
        else:
            messages.error(request,'invalid credentials')
            return redirect(adminLogin)

    return render (request,'login_admin.html')


def adminLogout(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    return redirect(adminLogin)


@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def admin_home(request):
    if 'username' in request.session:
        return render(request,'index_admin.html')

    return redirect(adminLogin)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def admin_table(request):
    if 'username' in request.session:
        value = Account.objects.all().order_by('id')
        p = Paginator(value,9)
        page = request.GET.get('page')
        values = p.get_page(page)

        return render(request,'admintable.html',{'values':values})

    return redirect(adminLogin)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def productList(request):
    if 'username' in request.session:
        values = Product.objects.all().order_by('-id')

        #setup pagination
        p = Paginator(values,3)
        page = request.GET.get('page')
        productValues =p.get_page(page)

        return render(request,'productslist.html', {'values' : values ,'productValues' : productValues})

    return redirect(adminLogin)



@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def categoryList(request):
    if 'username' in request.session:
        values = Categoryies.objects.all().order_by('id')
        return render(request,'categories.html',{'values':values})
    return redirect(adminLogin)


def editproduct(request,id):

    this_product = Product.objects.get(id=id)
    values = Categoryies.objects.all()

    if request.method == 'POST':

        product_name = request.POST.get('name')
        product_description = request.POST.get('description')
        product_price = request.POST.get('price')
        product_stock = request.POST.get('stock')
        # product_category = request.POST.get('category')
        product_image = request.POST.get('image')
        product_image1 = request.POST.get('image1')
        product_image2 = request.POST.get('image2')


        obj = Product.objects.get(id=id)

        obj.name = product_name
        obj.description = product_description
        obj.price = product_price
        obj.stock = product_stock
        # obj.category = product_category
        obj.image = product_image
        obj.image1 = product_image1
        obj.image2 = product_image2


        obj.save()
        return redirect(productList)
    return render(request,'useredit.html',{'this_product': this_product,'values':values})

       

def deleteproduct(request,id):
    if request.method == "POST":

        print("tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
        my_product =Product.objects.get(id=id)
        my_product.delete()
        return redirect(productList)



def addproduct(request):
    values = Categoryies.objects.all()
    if request.method == "POST":
        product_name = request.POST.get('name')
        product_description = request.POST.get('description')
        product_price = request.POST.get('price')
        product_stock = request.POST.get('stock')
        categ       = request.POST.get('category')
        

        product_image = request.POST.get('image')
        product_image1 = request.POST.get('image1')
        product_image2 = request.POST.get('image2')

        product = Product(name = product_name ,description =product_description,price=product_price,
        stock= product_stock,image=product_image,image1=product_image1,image2=product_image2 )
        product.category  = Categoryies.objects.get(id=categ)
        product.save()
        return redirect(productList)
    
    
    return render (request,'addproduct.html',{'values':values})

  
def addcategory(request):
    
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        offer = request.POST.get('offer')

        
        cat = Categoryies(category_name=category_name,description=description,offer=offer)
        
        cat.save()
        return redirect(categoryList)
    
    
    return render (request,'addcategory.html')

  
def deletecategory(request,id):
    my_cat = Categoryies.objects.get(id=id)
    my_cat.delete()
    return redirect(categoryList)


def blockuser(request,id):
    user = Account.objects.get(id = id)
    if user.is_active:
        user.is_active = False
       
    else:
        user.is_active = True
       
    user.save()
    return redirect(admin_table)


def orderdisplay(request):
    order= Orders.objects.all().order_by('-id')
    p = Paginator(order,9)
    page = request.GET.get('page')
    orders = p.get_page(page)
    
    return render(request,'orderadmin.html',{ 'order':order,'orders':orders})

def ordercanceladmin(request,id):
    
    order = Orders.objects.get(id = id)
    order.status = 'Cancelled'
    order.save()

    return redirect(orderdisplay)

    

def orderstatus(request,id):
    if request.method == "POST":
        status = request.POST.get('status')
    
        order = Orders.objects.get(id = id)
        order.status = status
        order.save()

    return redirect(orderdisplay)
def offerstatus(request,id):
    if request.method == "POST":
        status = request.POST.get('offer')
    
        categ = Categoryies.objects.get(id = id)
        categ.offer = status
        categ.save()

    return redirect(categoryList)

def  searchprod(request):
    try:
        q = request.GET['search']

        data = Product.objects.all()
        datas = []
    
        for i in data :
            datas.append(i.name)

        for i in datas:
           if q.lower() in i.lower():
               searched = Product.objects.filter(name = i)

        print(searched)

        return render(request, 'searcheditem.html',{'searched':searched})
    except:
        return render(request,'noproduct.html')


from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

from accounts.models import Account
from orders.models import Orders
from theproducts.models import Product , Categoryies
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator


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
        values = Account.objects.all()
        return render(request,'admintable.html',{'values':values})

    return redirect(adminLogin)

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def productList(request):
    if 'username' in request.session:
        values = Product.objects.all()

        #setup pagination
        p = Paginator(Product.objects.all(),3)
        page = request.GET.get('page')
        productValues =p.get_page(page)

        return render(request,'productslist.html', {'values' : values ,'productValues' : productValues})

    return redirect(adminLogin)



@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def categoryList(request):
    if 'username' in request.session:
        values = Categoryies.objects.all()
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

        obj = Product.objects.get(id=id)

        obj.name = product_name
        obj.description = product_description
        obj.price = product_price
        obj.stock = product_stock
        # obj.category = product_category
        obj.image = product_image

        obj.save()
        return redirect(productList)
    return render(request,'useredit.html',{'this_product': this_product,'values':values})

       

def deleteproduct(request,id):
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
        product = Product(name = product_name ,description =product_description,price=product_price,
        stock= product_stock,image=product_image )
        product.category  = Categoryies.objects.get(id=categ)
        product.save()
        return redirect(productList)
    
    
    return render (request,'addproduct.html',{'values':values})

  
def addcategory(request):
    
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        
        cat = Categoryies(category_name=category_name,description=description)
        
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
    order= Orders.objects.all().order_by('id')

    return render(request,'orderadmin.html',{ 'order':order })

def ordercanceladmin(request,id):
    
    order = Orders.objects.get(id = id)
    order.status = 'Cancelled'
    order.save()

    return redirect(orderdisplay)
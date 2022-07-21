from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminLogin),
    path('adminhome',views.admin_home,name='adminhome'),
    path('admintable',views.admin_table),
    path('productlist',views.productList),
    path('category',views.categoryList),
    path('editproduct/<int:id>/',views.editproduct),
    path('delete/<int:id>/',views.deleteproduct),
    path('addproduct',views.addproduct), 
    path('signout',views.adminLogout),  
    path('addcategory',views.addcategory) ,
    path('deletecategory/<int:id>/',views.deletecategory),
    path('blockuser/<int:id>/',views.blockuser),
    path('orderdisplay',views.orderdisplay,name='orderdisplay') , 
    path('ordercanceladmin/<int:id>/',views.ordercanceladmin,name='ordercanceladmin') , 

] 

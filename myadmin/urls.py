from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminLogin),
    path('adminhome',views.admin_home,name='adminhome'),
    path('admintable',views.admin_table,name='admintable'),
    path('productlist/',views.productList, name='productlist'),
    path('category',views.categoryList,name='category'),
    path('editproduct/<int:id>/',views.editproduct,name='editproduct'),
    path('delete/<int:id>/',views.deleteproduct,name='delete'),
    path('addproduct',views.addproduct,name='addproduct'), 
    path('signout',views.adminLogout),  
    path('addcategory',views.addcategory) ,
    path('deletecategory/<int:id>/',views.deletecategory,name='deletecategory'),
    path('blockuser/<int:id>/',views.blockuser),
    path('orderdisplay',views.orderdisplay,name='orderdisplay') , 
    path('ordercanceladmin/<int:id>/',views.ordercanceladmin,name='ordercanceladmin') ,
    path('orderstatus/<int:id>/',views.orderstatus,name='orderstatus')  ,
    path('offerstatus/<int:id>/',views.offerstatus,name='offerstatus')  ,
    path('searchprod',views.searchprod,name='searchprod')  , 

 


] 

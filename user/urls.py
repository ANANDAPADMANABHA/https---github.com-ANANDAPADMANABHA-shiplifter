from django.urls import path
from . import views

urlpatterns = [
    path('',views.home ,name='userhome' ),
    path('signinuser',views.signin,name='signinuser'),
    path('usersignup',views.userSignup), 
    path('usersignin',views.userSignin ,name='usersignin'),
    path('otp',views.otplogin),
    path('otpenter',views.otpverify),
    path('singnupuser',views.userSignup),
    path('userlogout',views.userlogout,name='userlogout'),
    path('productdisplay<int:id>',views.productDisplay) ,
    path('userprofile',views.userprofile,name='userprofile'), 
    path('myorders',views.myorders,name='myorders'), 
    path('ordercancel/<int:id>/',views.ordercancel,name='ordercancel') ,
    path('changepassword',views.changepassword,name='changepassword'),  




]
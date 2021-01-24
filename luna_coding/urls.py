from os import name
from django.urls import path 
from .views import * 

urlpatterns = [
    path('', HomePage , name='Home'),
    path('SignIn', SignInPage , name='signin-page'),
    path('SignUp', SignUpPage , name='signup-page'),
    path('Register', Register , name='Register'),
    path('Login', Login , name='Login'),
    path('SingOut', SingOut , name='SingOut'),
    path('DashBoard', DashBoard , name='DashBoard'),
    path('Profile', ProfilePage , name='Profile'),
]

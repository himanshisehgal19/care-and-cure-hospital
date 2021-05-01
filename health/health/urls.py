"""health URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from health_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.base,name='base'),
    #path('login/',views.login,name='login'),
    #path('sign_up/',views.sign_up,name='sign_up'),
    path('handle_signup/',views.handle_signup,name='handle_signup'),
    path('user_login/',views.user_login,name="user_login"),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('disease/',views.dise,name='disease'),
    path('prediction/',views.prediction,name='prediction'),
    path('disease_pre/',views.disease_with_details,name='disease_with_details'),
    path('doctor/',views.doctor,name='doctor'),
    path('consult/',views.consult,name='consult'),
    path('doctor_login/',views.doctor_login,name='doctor_login'),
    path('doctorpred/',views.doctorpred,name='doctorpred'),
    path('doctordisease/',views.doctordisease,name='doctordisease'),
    path('doctor_main/',views.doctor_main,name='doctor_main'),
    path('user_app/',views.user_app,name='user_app'),
    path('table/',views.table,name='table'),
    path('doctor_logout/',views.doctor_logout,name='doctor_logout'),
    path('without_app/',views.without_app,name='without_app'),
]

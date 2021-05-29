from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier as ds
from sklearn.naive_bayes import GaussianNB
from health_app.models import *
import pandas as pd
import numpy as np
from collections import Counter
from django.contrib.auth.models import User 
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from health_app.models import *
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import joblib
model=joblib.load("modelrfc.pkl")
modelsvm=joblib.load("modelsvm.pkl")
modelnb=joblib.load("modelnb.pkl")


def base(request):
    all_d=doctorlogin.objects.all().order_by('doctor')
    #print('your email is',request.session.get('email'))
    con={'all_d':all_d }
    return render(request,'base.html',con)
# Create your views here.
@login_required
def user_logout(request):
    logout(request)
    messages.success(request,'You have been logged out')
    return HttpResponseRedirect(reverse('user_login'))

def doctor_logout(request):
    messages.success(request,'You have been logged out')
    return HttpResponseRedirect(reverse('user_login'))
    


def handle_signup(request):

    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # checks
        if pass1!=pass2:  
            messages.error(request,'Passwords do not match')
            return redirect('/handle_signup')
        #Create the user
        myuser=User.objects.create_user(username,email,pass1)

        messages.success(request,"Your account has been successfully created")
        return redirect("/user_login")
    else:
        return render(request,'handle_signup.html')
    
def user_login(request):
     
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=User.objects.get(email=username),password=password)
       

        if user:
            login(request,user)
            request.session['patient_id']=user.id
            request.session['email']=user.email
            return HttpResponseRedirect(reverse('base'))
            
        else:
            #print("Someone tried to login and failed")
            #print("Username: {} and password{}".format(username,password))
            messages.error(request,'Invalid login details supplied')
            return redirect('/user_login')
    else:
        return render(request,'user_login.html')




def dise(request):
    all_Disease=disease.objects.all()
    paginator=Paginator(all_Disease,8)
    page=request.GET.get('page')
    try:
        all_Disease=paginator.page(page)
    except PageNotAnInteger:
        all_Disease=paginator.page(1)
    except EmptyPage:
        all_Disease=paginator.page(page.num_pages)
    context_dict={'all_Disease':all_Disease,'page':page}
    return render(request,'disease.html',context=context_dict)

  
#patient
def prediction(request):
    r=False
    all_sym=symptoms.objects.all().order_by('sym')
    cs=train.objects.all().values()
    df=pd.DataFrame(cs)
    if request.method=='POST':
        var1=request.POST['symptoms1']
        var2=request.POST['symptoms2']
        var3=request.POST['symptoms3']
        var4=request.POST['symptoms4']
        df.drop('id',axis=1,inplace=True)
        a=df.columns[df.columns!='prognosis']
        
        dfnew=pd.DataFrame(columns=a)
        
        dfnew.loc[len(dfnew)] = 0
        #dfnew
        dfnew[var1]=1
        dfnew[var2]=1
        dfnew[var3]=1
        dfnew[var4]=1
        #dfnew

       
        predicted_disease1=model.predict(dfnew)
        predicted_disease1=predicted_disease1[0]
        predicted_disease2=modelsvm.predict(dfnew)
        predicted_disease2=predicted_disease2[0]
        predicted_disease3=modelnb.predict(dfnew)
        predicted_disease3=predicted_disease3[0]
        disease=[]
        disease.append(predicted_disease1)
        disease.append(predicted_disease2)
        disease.append(predicted_disease3)
        

        def Most_Common(lst):
            data = Counter(lst)
            return data.most_common(1)[0][0]
        predicted_disease=Most_Common(disease)
        r=True
        request.session['predicted_disease']=predicted_disease
      
        cont={'predicted_disease':predicted_disease,'all_sym':all_sym,'r':r}
    
        return render(request,'prediction.html',cont)
    else:
        co={'all_sym':all_sym}
        return render(request,'prediction.html',co)

#patient
def disease_with_details(request):
    all_Disease=disease.objects.all().values()
    all_food=medicines.objects.all().values()
    df=pd.DataFrame(all_food)
    dfx=pd.DataFrame(all_Disease)
    
    
    h=request.session.get('predicted_disease')
    dfy=df[df['Disease']==h]
    dfz=dfx[dfx['Disease']==h]
    a=dfz['image'].iloc[0]
    b=dfz['pre_one'].iloc[0]
    c=dfz['pre_two'].iloc[0]
    d=dfz['pre_three'].iloc[0]
    e=dfz['detail'].iloc[0]
    f=dfz['pre_four'].iloc[0]
    nut1=dfy['nutrient_1'].iloc[0]
    nut2=dfy['nutrient_1'].iloc[0]
    nut1=str(nut1)
    nut2=str(nut2)
    food=''
    g=''
    i=''
    li=[]
    items1=''
    items2=''
    items3=''
    items4=''    
    if nut1=='' and nut2=='':
        food=dfy['food'].iloc[0]
        li=food.split(';')    
    elif nut2=='':
        g=dfy['nutrient_1'].iloc[0]
        i=dfy['nutrient_1'].iloc[0]
    else:
        g=dfy['nutrient_1'].iloc[0]
        i=dfy['Nutrient_2'].iloc[0]
    if li[0]:
        items1=li[0]
    else:
        items1=''
    if li[1]:
        items2=li[1]
    else:
        items2=''
    if li[2]:
        items3=li[0]
    else:
        items3=''
    if li[3]:
        items4=li[0]
    else:
        items4=''
   
   
    con={'h':h,'all_Disease' :all_Disease,'a':a,'b':b,'c':c,'d':d,'e':e,'f':f,'g':g,'i':i,'food':food,'items1':items1,'items2':items2,'items3':items3,'items4':items4}
    return render(request,'disease_pre.html',con)

#doctor
def doctor(request):
    all_doctors=Doctor.objects.all().order_by('doctor')
    all_Disease=disease.objects.all().values()
    all_food=medicines.objects.all().values()
    dm=pd.DataFrame(all_food)
    doc=disease.objects.all().values()
    df=pd.DataFrame(all_Disease)
    h=request.session.get('predicted_disease_d')
    dfx=pd.DataFrame(doc)
    dfz=dfx[dfx['Disease']==h]
    dff=df[df['Disease']==h]
    ss=dm[dm['Disease']==h]
    j=dff['image'].iloc[0]
    a=dfz['lines'].iloc[0]
    g=ss['nutrient_1'].iloc[0]
    i=ss['Nutrient_2'].iloc[0]

    con={'h':h,'all_doctors' :all_doctors,'a':a,'g':g,'i':i,'j':j}
    return render(request,'doctors.html',con)

#patient
def consult(request):
    h=request.session.get('predicted_disease')
    l=request.session.get('email')
    all_food=medicines.objects.all().values()
    all_doctors=doctorlogin.objects.all().values()
    all_d=doctorlogin.objects.all().order_by('doctor')
    
    df=pd.DataFrame(all_doctors)
    #print(df)
    dfx=pd.DataFrame(all_food)
    dfz=dfx[dfx['Disease']==h]
    a=dfz['doctors'].iloc[0]
    dfk=df[df['specialisation']==a]
    li=[]
    for i in dfk['doctor']:
        li.append(i)
    


    
    con={'all_doctors':all_doctors,'all_d':all_d,'h':h,'li':li,'dfk':dfk,'a':a}
    
    return render(request,'consult.html',con)

def doctor_login(request):
    r=False
    df=pd.read_csv('doctor_login.csv')
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        request.session['email']=email
        if password=='doctor@1928' and email in df.values:
            r=True
            con={'r':r}
            
            return render(request,'doctor_main.html',con)
        else:
            messages.error(request,'Invalid credentials')
            return redirect('/doctor_login')
    else:
        return render(request,'doctor_login.html')
#doctor
def doctorpred(request):
    r=True
    all_sym=symptoms.objects.all().order_by('sym')
    cs=train.objects.all().values()
    df=pd.DataFrame(cs)
    if request.method=='POST':
        var1=request.POST['symptoms1']
        var2=request.POST['symptoms2']
        var3=request.POST['symptoms3']
        var4=request.POST['symptoms4']
        df.drop('id',axis=1,inplace=True)
        a=df.columns[df.columns!='prognosis']
        
        dfnew=pd.DataFrame(columns=a)
        
        dfnew.loc[len(dfnew)] = 0
        #dfnew
        dfnew[var1]=1
        dfnew[var2]=1
        dfnew[var3]=1
        dfnew[var4]=1
        #dfnew
       
        predicted_disease_d=model.predict(dfnew)
        predicted_disease_d=predicted_disease_d[0]
        request.session['predicted_disease_d']=predicted_disease_d
        cont={'predicted_disease_d':predicted_disease_d,'all_sym':all_sym,'r':r}
        #conte={"reldis":reldis,"reldis2":reldis2,"reldis":reldis3,'all_sym':all_sym}
        return render(request,'doctorpred.html',cont)
    else:
        co={'all_sym':all_sym}
        return render(request,'doctorpred.html',co)

#doctor
def doctordisease(request):
    all_Disease=disease.objects.all().values()
    all_food=medicines.objects.all().values()
    df=pd.DataFrame(all_food)
    dfx=pd.DataFrame(all_Disease)
    
    
    h=request.session.get('predicted_disease_d')
    dfy=df[df['Disease']==h]
    dfz=dfx[dfx['Disease']==h]
    varx=dfy['medicine'].iloc[0]
    
    splitlist = varx.split(",")
    med1=splitlist[0]
    med2=splitlist[1]
    med3=splitlist[2]
    med4=splitlist[3]
    image_one=dfy['image_one'].iloc[0]
    image_two=dfy['image_two'].iloc[0]
    image_three=dfy['image_three'].iloc[0]
    image_four=dfy['image_four'].iloc[0]

    detail=dfy['lines'].iloc[0]
    
    a=dfz['image'].iloc[0]
    b=dfz['pre_one'].iloc[0]
    c=dfz['pre_two'].iloc[0]
    d=dfz['pre_three'].iloc[0]
    e=dfz['detail'].iloc[0]
    f=dfz['pre_four'].iloc[0]
    nut1=dfy['nutrient_1'].iloc[0]
    nut2=dfy['nutrient_1'].iloc[0]
    nut1=str(nut1)
    nut2=str(nut2)
    food=''
    g=''
    i=''
    li=[]
    items1=''
    items2=''
    items3=''
    items4=''    
    if nut1=='' and nut2=='':
        food=dfy['food'].iloc[0]
        li=food.split(';')    
    elif nut2=='':
        g=dfy['nutrient_1'].iloc[0]
        i=dfy['nutrient_1'].iloc[0]
    else:
        g=dfy['nutrient_1'].iloc[0]
        i=dfy['Nutrient_2'].iloc[0]
    if len(li)>0:
        items1=li[0]
        items2=li[1]
        items3=li[2]
        items4=li[3]
    #print(li)
    
    #print(a)
    #print(dfz)
    #print(h)

    con={'h':h,'all_Disease' :all_Disease,'a':a,'b':b,'c':c,'d':d,'e':e,'f':f,'g':g,'i':i,'med1':med1,'med2':med2,'med3':med3,'med4':med4,'image_one':image_one,'image_two':image_two,'image_three':image_three,'image_four':image_four,'detail':detail,'food':food,'items1':items1,'items2':items2,'items3':items3,'items4':items4}
    return render(request,'doctordisease.html',con)

def doctor_main(request):
    return render(request,'doctor_main.html')



def user_app(request):
    all_doctors=doctorlogin.objects.all().values()
    
    df=pd.DataFrame(all_doctors)
    if request.method=="POST":
        phone=request.POST['phone']
        address=request.POST['address']
        patient_name=request.POST['patient_name']
        message=request.POST['message']
        age=str(request.POST['age'])
        date=request.POST['date']
        doctor=request.POST['doctor']
        user1 = request.user.get_username()
        email=request.session.get('email')
        dfy=df[df['doctor']==doctor]
        em=dfy['email'].iloc[0]
        
        new_entry= Appoint(
                user_name = user1,
                email_patient =email ,
                doctor_name = doctor,
                doctor_email = em,
                appointment_date=date,
                phone_number=phone,
                address=address,
                patient_name=patient_name,
                message= message,
                age=age,
                
            )
            
        new_entry.save()
        messages.success(request, "Your appointment request has been sent successfully. Thank you!")
        return redirect("/consult")
    

def table(request):
    email=request.session.get('email')
    all_objects=Appoint.objects.all().values()
    all_obj=Appoint.objects.all()
    df=pd.DataFrame(all_objects)
    dfz=df[df['doctor_email']==email]
   # print(dfz)
   
    
    con={'all_objects':all_objects,'all_obj':all_obj,'dfz':dfz}
    return render(request,'table.html',con)


def without_app(request):
    all_doctors=doctorlogin.objects.all().values()
    
    df=pd.DataFrame(all_doctors)
    if request.method=="POST":
        phone=request.POST['phone']
        address=request.POST['address']
        patient_name=request.POST['patient_name']
        message=request.POST['message']
        age=str(request.POST['age'])
        date=request.POST['date']
        doctor=request.POST['doctor']
        email=request.POST['email']
        dfy=df[df['doctor']==doctor]
        em=dfy['email'].iloc[0]
        
        new_entry = Appoint(
                user_name=patient_name,
                email_patient =email ,
                doctor_name = doctor,
                doctor_email = em,
                appointment_date=date,
                phone_number=phone,
                address=address,
                patient_name=patient_name,
                message= message,
                age=age,
                
            )
            
        new_entry.save()
        messages.success(request, "Your appointment request has been sent successfully. Thank you!")
        return redirect("/")
     




from django.shortcuts import render,HttpResponse,redirect
from .models import property_cat,property,book,property_rent,booking,customer_details,rent
from .forms import propertyform,registrationform,propertydetailsform,UserauthenticationFormm,property_rent_form,Customer_detailsform,FeedbackForm
import datetime
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views import View
from django.conf import settings
import uuid
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView  
from django.views.generic.edit import UpdateView 

from django.urls import reverse_lazy
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import properserializer

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from django.contrib import messages

from django.conf import settings
import datetime
########### login view##############
def logindetails(request):
     if request.method=="POST":
        uemail=request.POST["email"]
        upass=request.POST["password"]
        users = get_user_model().objects.filter(email=uemail)
        for user in users:
            if user.check_password(upass):
                user=user
        if user is not None:
            login(request,user)
            response=redirect('home')
            request.session['email']=uemail
            response.set_cookie('email',uemail)

            response.set_cookie('time',datetime.datetime.now())
            return response            
        else:
             fm=UserauthenticationFormm()

             return render(request,'login.html',{'forms':fm,'msg':'wrong Credentials!!'})

     else:
         fm=UserauthenticationFormm()
         print(fm)
         return render(request,'login.html',{'forms':fm})  

#########logout view##################
def logoutdetails(request):
    logout(request)
    return redirect('home')

########register view################
def register(request):
    if request.method == "POST":
        form = registrationform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = registrationform()
    return render(request, 'register.html', {"forms": form})


###########index page view ####################
def show(request):
    proper=property_cat.objects.all()
    pro=property.objects.all()
    rent=property_rent.objects.filter(rented=False)
    context={}
    context['pro']=pro
    context['proper']=proper
    context['rent']=rent

    return render(request,'index.html',context)

#########search property########################
def searchproperty(request):
    if request.method=="POST":
        data=request.POST['search']

        searchdata=property_rent.objects.filter(title__icontains=data)
        return render(request,'search.html',{'searchdata':searchdata})
    

    else:
        return redirect('home')


def properties_view(request,id):
    proper=property_cat.objects.all()
    pro=property.objects.filter(pro_cat=id)
    context={}
    context['proper']=proper
    context['pro']=pro

    return render(request,'buy.html',context)


def visitpro(request,id):
    pro=property.objects.filter(id=id)
    context={}
    context['pro']=pro
    return render(request,'product.html',context)

def propertyview(request):
    if request.method=="POST":
    
       fm=propertyform(request.POST)
       if fm.is_valid():
           return HttpResponse("DATA IS SAVED")
       
    else:

        fm=propertyform()
        return render (request,"propertyform.html",{'forms':fm})



# class user_login(View):
#     def get(request):
#          fm=UserauthenticationForm()
#          return render(request,'login.html',{'forms':fm})


#     def post(request):
#       if request.method=="POST":
#          uname=request.POST["username"]
#          upass=request.POST["password"]
#          user=authenticate(request,username=uname,password=upass)
#          if user is not None:
#             login(request,user)
            
#             response=render(request,'index.html',{'username':uname})
#             request.session['username']=uname
#             response.set_cookie('username',uname)

#             response.set_cookie('time',datetime.datetime.now())
#             return response            
#          else:
#              fm=UserauthenticationForm()

#              return render(request,'login.html',{'forms':fm,'msg':'wrong Credentials!!'})

"""def propertydetails(request):
    if request.method=="POST":
        ap=propertydetailsform(request.POST,request.FILES)
        print(ap.data)
        if ap.is_valid():
            ap.save()
            return HttpResponse("Successfully saved")
        else:
            return HttpResponse("False")
    else:
        ap=propertydetailsform()
        return render(request,'propertyform.html',{'ap':ap})"""


def propertydetails(request):
    try:
        if request.method == "POST":
            # Create a form instance with POST data and uploaded files
            ap = propertydetailsform(request.POST, request.FILES)
            print(ap.data)  # Optional: To see the form data in the console

            if ap.is_valid():
                # Save the form if it's valid
                ap.save()
                return HttpResponse("Successfully saved")
            else:
                # Return an error if the form is invalid
                return HttpResponse(f"Form is not valid.{ap.errors}")
        else:
            # If the method is GET, instantiate an empty form
            ap = propertydetailsform()
            return render(request, 'propertyform.html', {'ap': ap})

    except Exception as e:
        # Catch any exceptions and print the error message
        print(f"An error occurred: {e}")
        return HttpResponse(f"An error occurred: {e}")




@login_required(login_url='login')
def bookproperty(request,pid):
    if request.user.is_authenticated:
       userid=request.user.id
       u=User.objects.filter(id=userid)
       p=property.objects.filter(id=pid)
       q1=Q(uid=u[0])
       b=book.objects.filter(Q(uid=u[0]) & Q(pid=p[0]))
       print(b)
       n=len(b)
       context={}
       context={'pro':p}
       if n==1:
           context['msg']='property is already in  booking list'
           return render(request,'product.html',context)
       else:
           b=book.objects.create(uid=u[0],pid=p[0])
           b.save()
           context['success']='property added successfully to book'
           return render(request,"product.html",context)



@login_required(login_url='login')
def bookrentproperty(request,pid):
    if request.user.is_authenticated:
       userid=request.user.id
       u=User.objects.filter(id=userid)
       p=property_rent.objects.filter(id=pid)
       q1=Q(uid=u[0])
       b=rent.objects.filter(Q(uid=u[0]) & Q(pid=p[0]))
       print(b)
       n=len(b)
       context={}
       context={'data':p}
       if n==1:
           context['msg']='property is already in  booking list'
           return render(request,'rentpropertyview.html',context)
       
       else:
           b=rent.objects.create(uid=u[0],pid=p[0])
           b.save()
           context['success']='property added successfully to book'
           return render(request,"rentpropertyview.html",context)
def viewproperty(request): 
       userid=request.user.id
       print(userid)
       data=book.objects.filter(uid=userid)
       to_buy = []
       total=0
       for i in data:
            property1 =property.objects.filter(id = i.pid.id, rented = False).first()    
            if property1:
             prop=data.filter(pid = property1.id).first()
             to_buy.append(prop)
            else:
               continue

            context={}
            context['data']=data
            return render(request,"book.html",context)




def viewrentproperty(request): 
        userid=request.user.id
        print(userid)
        data=rent.objects.filter(uid=userid)
        to_rent = []
        total=0
        for i in data:
            property = property_rent.objects.filter(id = i.pid.id, rented = False).first()
            if property:
                prop=data.filter(pid = property.id).first()
                to_rent.append(prop)
            else:
               continue
        context={}
        context['data']=to_rent
        print('here', context)
        return render(request,"rentpropertycart.html",context)
    


def remove_property(request,id): 
    c= book.objects.filter(uid=request.user.id, pid=id).first()
    c.delete()
    return redirect('viewproperty')
#######################rent property remove#####################
def remove_rentproperty(request,id): 
    c= rent.objects.filter(uid=request.user.id, pid=id).first()
    c.delete()
    return redirect('viewrentproperty')

def updateproperty(request,qv,cid):
    print(cid)
    print(qv)
    data=book.objects.filter(id=cid)
    if qv==1:
        total_quantity=data[0].qty+1
        data.update(qty=total_quantity)
    else:

         if data[0].qty>1:
    
           total_quantity=data[0].qty-1
           data.update(qty=total_quantity)
 
    return redirect('/viewproperty')


def rent_property(request):
     rent=property_rent.objects.all()
     context={}
     context['rent']=rent

     return render(request,"rent_property.html",context)


def buy_property(request):
    pro=property.objects.all()
    context={}
    context['pro']=pro
    return render(request,"buy.html",context)








#############cookies session view#############
def set_cookie(request):
    response=HttpResponse("cookie set")
    response.set_cookie('username','Priya')
    return response

def get_cookie(request):
    username=request.COOKIES.get('username')
    
    print(username)
    return render(request,'getcookie.html',{'username':username})

############contact us#############


def contactus_form(request):
    return render(request,'contactus.html')


def rentpropertydetails(request):
    if request.method=="POST":
        ap=property_rent_form(request.POST,request.FILES)
        if ap.is_valid():
            ap.save()
        return HttpResponse("Successfully saved")


    else:
        ap=property_rent_form()
        return render(request,'propertyrentform.html',{'ap':ap})
    

def rent_propertydetails(request,id): 

       data=property_rent.objects.filter(id=id)
       total=0
       for x in data:
           total=total+x.price 
       context={}
       context['data']=data
       context['total']=total
       rentview=property_rent.objects.filter().exclude(id=id)
       context['rentview']=rentview

       return render(request,"rentpropertyview.html",context)

def single_rent_checkoutview(request, pid):
    userid=request.user.id
    c=rent.objects.filter(uid=userid, pid=pid).first()

    total_price = c.pid.price
    
    
    host = request.get_host()

    paypal_checkout = {
        'business' : settings.PAYPAL_RECEIVER_EMAIL,
        'amount' :total_price,
        'property_name':'property',
        'invoice':uuid.uuid4(),
        'current_code':'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url' : f"http://{host}{reverse('paymentsuccess', args=[c.pid.id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
        }
    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    
    return render(request,'checkout1.html',{'total_price':total_price,'cart_data':c,'paypal':paypal_payment})






def checkoutview(request, pid):
       userid=request.user.id
       c=book.objects.filter(uid=userid, pid=pid).first()
       total_price = c.pid.pro_price
    
      
       host = request.get_host()

       paypal_checkout = {
            'business' : settings.PAYPAL_RECEIVER_EMAIL,
            'amount' :total_price,
            'property_name':'property',
            'invoice':uuid.uuid4(),
            'current_code':'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
           'return_url' : f"http://{host}{reverse('paymentsuccess', args=[c.pid.id])}",
            'cancel_url': f"http://{host}{reverse('paymentfailedbuy')}",
           }
       paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
        
       return render(request,'checkout.html',{'total_price':total_price,'cart_data':c,'paypal':paypal_payment})

def paymentsuccessbuy(request, pid):
    rented_property = property.objects.filter(id=pid).first()
    rented_property.rented = True
    rented_property.save()
    return render(request,'paymentsuccessbuy.html')



# def checkoutview1(request):
#        userid=request.user.id
#        c=rent.objects.filter(uid=userid)
#        total=0
       
#        for x in c:
#          print (x.pid)
#          print (x.uid)
     
#          total_price=total+x.pid.price
#        print(total_price)
       
      
#        host = request.get_host()

#        paypal_checkout = {
#             'business' : settings.PAYPAL_RECEIVER_EMAIL,
#             'amount' :total_price,
#             'property_name':'property',
#             'invoice':uuid.uuid4(),
#             'current_code':'USD',
#             'notify_url': f"http://{host}{reverse('paypal-ipn')}",
#             'return_url' : f"http://{host}{reverse('paymentsuccess')}",
#             'cancel_url': f"http://{host}{reverse('paymentfailed')}",
#            }
#        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
        
#        return render(request,'checkout1.html',{'total_price':total_price,'cart_data':c,'paypal':paypal_payment})




def forget_password(request):
    if request.method =='POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user: 
            
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = request.build_absolute_uri(f'/reset_password/{uidb64}/{token}/')
                                                   
            send_mail(
            'Password Reset',
            f'Click the given link to reset your password: {reset_url}',
            settings.EMAIL_HOST_USER, # Use a verified email address
            [email],
            fail_silently=False,
             )
            return redirect('passwordresetdone')
        else:
           
           
           messages.success(request,'please enter valid email address')

    return render(request,'forgetpass.html')

def reset_password(request, uidb64, token):

    if request.method == 'POST':
       
       password = request.POST['password']
       print(password)
       password2 = request.POST['password2']
       print(password2)
       if password == password2:  
        try:
      
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
             
             user.set_password(password)
             user.save()
             return redirect('passwordresetdone')
            else: 
             return HttpResponse('Token is invalid',status=400)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
           return HttpResponse('Invalid link', status=400)
       else:
          
          return HttpResponse('Passwords do not match', status=400)
    return render(request,'password_rest.html')


def password_reset_done(request):
    return render (request,'password_reset_done.html')

      
        
        
   
def paymentsuccess(request, pid):
    rented_property = property_rent.objects.filter(id=pid).first()
    rented_property.rented = True
    rented_property.save()
    return render(request,'paymentsuccess.html')




def paymentfailedbuy(request):
    return render(request,'paymentfailedbuy.html')

def paymentfailed(request):
    return render(request,'paymentfailed.html')





def customer_address(request):

     if request.method=="POST":
       
       fm=Customer_detailsform(request.POST)
       name=request.POST['name']
       city =request.POST['city']
       state = request.POST['state']
       pincode=request.POST['pincode']
       context={}
       if name=="" or city=="" or state=="":

          context['errmsg']="Field cannot be empty"
          return render(request,'address.html',context)
       if fm.is_valid():
          data=fm.save(commit=False)
          data.user=request.user
          data.save()
          return redirect('home')
     else:
       mf =Customer_detailsform()
       return render(request,'address.html',{'form':mf})

def checkout(request):
    cust_deatils=customer_details.objects.filter(user=request.user)
    return render(request,'checkout.html',{'cust_details':cust_deatils})
   



class PostListView(ListView):
    model= property
    template_name = 'show_property.html'
    context_object_name ='posts'
    paginate_by = 10




class PostCreateView(CreateView):
    model = customer_details
    fields = ['user','Name','address','city','pincode']
    template_name= 'show_property.html'
    success_url= reverse_lazy('showlist')


class PostUpdateView(UpdateView):
    model = customer_details
    fields = ['user','Name','address','city','pincode']
    template_name= 'show_property.html'
    success_url= reverse_lazy('showlist')

#  # retal properties in indexpage

 
class crud_api(APIView):
 
 def post(self,request):
        data=request.data
        print(data)
        serializer=properserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success":"data is successfully saved"},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

 def get(self,request):
        id=request.data.get('id',None)
        print(id)
        if id:
            try:
                properties_data=property.objects.get(id=id)
                serializer=properserializer(properties_data)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except:
                return ResourceWarning({"ERROR":"id is not found"},status=status.HTTP_404_NOT_FOUND)
        
        else:
            properties_data=property.objects.all()
            print(properties_data)
            serializer=properserializer(properties_data,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
            
def patch(self,request):
        update_data=request.data
        print(update_data)
        id=request.data.get("id")
        if id:
             
             properties_data=rentpropertydetails.get(id=id)
             print( properties_data)
             serializer=properserializer(properties_data,update_data,partial=True)
             if serializer.is_valid():
                 serializer.save()
                 return Response({"Successs":"data update successfully"},status=status.HTTP_200_OK)
        

      
def delete(self,request):
        id=request.data.get("id")
        print(id)
        properties_data=property.get(id=id)
        if id:
            properties_data.delete()
            return Response({"success":"successfully deleted"},status=status.HTTP_200_OK)
 



from .forms import FeedbackForm

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')  # Redirect to a 'Thank You' page
    else:
        form = FeedbackForm()

    return render(request, 'feedback_form.html', {'form': form})


def thank_you(request):
    return render(request, 'feedback/thank_you.html')








# rent property crud#

def managerentproperty(request):
    data=property_rent.objects.all()
    
    context={}
    context['data']=data
    return render(request,'managerentproperty.html',context)

def update_rent_property(request,id):
    product = property_rent.objects.get( id=id)
    
    if request.method == "POST":
        FM = property_rent_form(request.POST,request.FILES,instance=product)  
        if FM.is_valid():
            FM.save()  
            return redirect('managerentproperty')
        else:
            return render(request, "update_rent_property.html", {"FM": FM, "errors": FM.errors})  
    else:
        FM = property_rent_form(instance=product) 
    return render(request, "update_rent_property.html", {"FM": FM})
    

def delete_rent_property(request, id):
    deletepro=property_rent.objects.filter(id=id)
    deletepro.delete()
    return redirect('managerentproperty')







# buy property crud
def managebuyproperty(request):
    data=property.objects.all()
    
    context={}
    context['data']=data
    return render(request,'managebuyproperty.html',context)




def update_buy_property(request,id):
    product = property.objects.get( id=id)
    
    if request.method == "POST":
        FM = propertydetailsform(request.POST,request.FILES,instance=product)  
        if FM.is_valid():
            FM.save()  
            return redirect('managebuyproperty')
        else:
            return render(request, "update_buy_property.html", {"FM": FM, "errors": FM.errors})  
    else:
        FM = propertydetailsform(instance=product) 
    return render(request, "update_buy_property.html", {"FM": FM})
    

def delete_buy_property(request, id):
    deletepro=property.objects.filter(id=id)
    deletepro.delete()
    return redirect('managebuyproperty')



def paymentproperty(request):
    if request.user.is_authenticated:
        rent_pro=rent.objects.filter(uid=request.user.id)
        context={}
        context['rent_pro']=rent_pro
        return render(request,'paymentpropertysuccess.html',context)
        
    else:
        return redirect('login')
    


def buypaymentproperty(request):
    if request.user.is_authenticated:
        rent_pro=book.objects.filter(uid=request.user.id)
        context={}
        context['rent_pro']=rent_pro
        return render(request,'paymentpropertysuccessbuy.html',context)
        
    else:
        return redirect('login')
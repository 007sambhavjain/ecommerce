from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# Create your views here.
def choice(request):
    if request.method=='GET':
        curr=request.user
        if curr:
            if Customer.objects.filter(user=curr):
                return redirect('/store/')
            if Vendor.objects.filter(user=curr):
                return('/vendor/')
        else:
            return render(request,'main/choice.html')
    if request.method=='POST':
        curr=request.user
        
        usertype = request.POST.get('type')
        if usertype == 'customer':
            cust = Customer.objects.create(user=request.user)
            cust.save()
            return redirect('/store/')
        if usertype == 'vendor':
            venr = Vendor.objects.create(user=request.user)
            venr.save()
            return('/vendor/')

def sign_up(request):
    if request.method== 'GET':
#         message = Mail(
#             from_email='f20190255@pilani.bits-pilani.ac.in',
#             to_emails='f20190255@pilani.bits-pilani.ac.in',
#             subject='Sending with Twilio SendGrid is Fun',
#             html_content='<strong>and easy to do anywhere, even with Python</strong>')
#         try: 
#             sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#             response = sg.send(message)
#             print(response.status_code)
#             print(response.body)
#             print(response.headers)
#         # except Exception as e:
#         #     print(e.message)    
#         except:
#             print("akn")
        return render(request,'main/sign_up.html')

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')
        usertype = request.POST.get('type')

        if len(phone_number) != 10:
            return HttpResponse('Phone number must be 10 digits long')

        if User.objects.filter(username=username).exists():
            return HttpResponse('Username already taken!')
        
        user = User.objects.create_user(username=username, password=password)

        if usertype == 'customer':
            cust = Customer.objects.create(user=user, name=name, mobile_number=phone_number)
            cust.save()
        if usertype == 'vendor':
            venr = Vendor.objects.create(user=user, name=name, mobile_number=phone_number)
            venr.save()

        

        return render(request,'main/sign_up.html')

    
@csrf_exempt
def sign_in(request):

    if request.method=='GET':
        return render(request,'main/sign_in.html')

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
       
       
        if Customer.objects.filter(user=user):
            login(request,user)
            cust=Customer.objects.get(user=user)
            return redirect('/store/')
        if Vendor.objects.filter(user=user):
            login(request,user)
            vend=Vendor.objects.get(user=user)
            
            return redirect('/vendor/')  



def vendor_profile(request):
    if not request.user.is_authenticated:
        return HttpResponse('User is not authenticated!')

    curr=request.user
    if Vendor.objects.filter(user=curr):

        form = ProductForm()
        vend = Vendor.objects.get(user=curr)
        pro=Product.objects.filter(vendor=vend)

        if request.method == 'POST':
                # title = str(request.POST.get('title'))
    
                # content = str(request.POST.get('content'))
                # price = str(request.POST.get('price'))
        
                # vend = Vendor.objects.get(user=curr)
        

                # prod = Product.objects.create(title=title,cost=price, description=content, vendor=vend)
                form = ProductForm(request.POST)
                if form.is_valid():
                    product = form.save(commit=False)
                    product.vendor=vend
                    product.save()
                    return redirect('/vendor/')    

        
        return render(request,'main/vendor.html',{'pro': pro,'form':form})

def product(request,pk):
    if not request.user.is_authenticated:
        return HttpResponse('user not authenticated')

    prod=Product.objects.get(id=str(pk))
    form = ProductForm(instance=prod)
    if request.method=='POST':
        form = ProductForm(request.POST,instance=prod)
        if form.is_valid():
            form.save() 
            return redirect('/vendor/')  
        
    context={'form':form}

    # pro=Product.objects.get(id=str(pk))
    # # s=Product(instance=pro)
    # form = ProductForm() 
    return render(request,'main/product.html',context)


def delete_task(request,pk):
    item = Product.objects.get(id=str(pk))
    if request.method=='POST':
        item.delete()
        return redirect('/vendor')

    context={'item':item}
    return render(request,'main/delete.html',context)

def store(request):

    if not request.user.is_authenticated:
            return HttpResponse('User is not authenticated!')

    curr=request.user
    if Customer.objects.filter(user=curr):

        product=Product.objects.all()

        context={'product':product}
    
        return render(request,'main/store.html',context)


def cart(request,pk):
    # if request.user.is_authenticated:
    #     curr=request.user
    #     if Customer.objects.filter(user=curr):
    #         if request.method=='POST':
    #                 cust=Customer.objects.get(user=curr)
    #                 product=Product.objects.get(id=str(pk))
    #                 quan=request.POST.get('quantity')
                  

    #                 qe=w.quantity
    #                 total=float(qe)*w.product.cost                
            
    #         if request.method=='GET':
    #             cust=Customer.objects.get(user=curr)
    #             product=Product.objects.get(id=str(pk))
    #             quan=request.POST.get('quantity')
    #             order=Orderitem.objects.create(product=product,quantity=quan)
          
    #             # total=w.product.cost
    #         return render(request,'main/cart.html',{'':w})    
     if request.user.is_authenticated:
        curr=request.user
        if Customer.objects.filter(user=curr):
             if request.method=='GET':
                cust=Customer.objects.get(user=curr)
                product=Product.objects.get(id=str(pk))
                quan=request.POST.get('quantity')
                y=Orderitem.objects.filter(custom=cust,product=product)
                if y:
                    return redirect('/carts/')
                else:
                    order=Orderitem.objects.create(custom=cust,product=product,quantity=1,ven=product.vendor)
                   
                
                   

             items=Orderitem.objects.all().filter(custom=cust)
             tot=sum([item.total  for item in items])
             context={'items':items,'cust':cust,'tot':tot}

             return render(request,'main/cart.html',context)  
             
def quantity(request,pk):
    if request.user.is_authenticated:
        curr=request.user
        if Customer.objects.filter(user=curr):
            if request.method=='POST':
                cust=Customer.objects.get(user=curr)
                product=Product.objects.get(id=str(pk))
                quan=request.POST.get('quantity')
                order=Orderitem.objects.get(custom=cust,product=product)
                order.quantity=quan
                order.save()
                return redirect('/carts/')
                
            if request.method=='GET':    
                return render(request,'main/quantity.html')

def carts(request):
    if request.user.is_authenticated:
        curr=request.user
        if Customer.objects.filter(user=curr):
            cust=Customer.objects.get(user=curr)
            items=Orderitem.objects.all().filter(custom=cust)
            tot=sum([item.total  for item in items])
            
  
    context={'items':items,'cust':cust,'tot':tot}

    return render(request,'main/carts.html',context)  

             
def money(request):
     if request.user.is_authenticated:
        curr=request.user
        if Customer.objects.filter(user=curr):
            mon=request.POST.get('money')

            if request.method=='GET':  
                return render(request,'main/money.html')

            if request.method=='POST':  
                cust=Customer.objects.get(user=curr)
                cust.money+=float(mon)
                cust.save() 
                return redirect('/carts/')


def order(request):
     if request.user.is_authenticated:
        curr=request.user
        if Customer.objects.filter(user=curr):
            cust=Customer.objects.get(user=curr)
            order=Orderitem.objects.all().filter(custom=cust)
            tot=sum([it.total  for it in order])
        
            if request.method=='GET':
                return render(request,'main/order.html')

            if request.method=='POST':
                adress = request.POST.get('adress')
                city = request.POST.get('city')
                state = request.POST.get('state')
                if ShippingAddress.objects.filter(customer=cust,address=adress,city=city,state=state):  

                    ship=ShippingAddress.objects.get(customer=cust,address=adress,city=city,state=state)
                else:
                    ship=ShippingAddress.objects.create(customer=cust,address=adress,city=city,state=state)
                if cust.money>=tot:
                    for item in order:
                        if item.quantity!=0:
                            if item.product.quantity>=item.quantity  :
                                item.product.quantity-=item.quantity
                                item.product.save()
                            else:
                                return HttpResponse(str(item.product.title) + ' has only '+ str(item.product.quantity) + ' left. so cannot place order ')     
                        else:
                            return HttpResponse('cannot order 0 product')        
                else:
                    return HttpResponse("you don't have enough money") 

                cust.money-=tot
                cust.save()
                for item in order:
                    final=Order.objects.create(customer=cust,quantity=item.quantity,vend=item.ven,prod=item.product)
                    item.delete()
                
                return render(request,'main/final.html',{'ship':ship})    



def previous(request):   
    if request.user.is_authenticated:
        curr=request.user
        if Customer.objects.filter(user=curr):
            cust=Customer.objects.get(user=curr)
            order=Order.objects.all().filter(customer=cust) 


            return render(request,'main/previous.html',{'order':order})

    

def previous_vendor(request):   
    if request.user.is_authenticated:
        curr=request.user
        if Vendor.objects.filter(user=curr):
            ven=Vendor.objects.get(user=curr)
            order=Order.objects.all().filter(vend=ven) 


            return render(request,'main/previous_vendor.html',{'order':order})



    
def delet(request,pk):
    if request.user.is_authenticated:
        curr=request.user
        if Customer.objects.filter(user=curr):
            cust=Customer.objects.get(user=curr)
            product=Product.objects.get(id=str(pk))
            order=Orderitem.objects.get(custom=cust,product=product)
            if request.method=='POST':
                order.delete()
                return redirect('/carts/')
            if request.method=='GET':
                return render(request,'main/dele.html',{'order':order})
            

def sign_out(request):
    if not request.user.is_authenticated:
        return HttpResponse('User is not signed in, so he cannot sign out')

    logout(request)
    return HttpResponse('User has been logged out')

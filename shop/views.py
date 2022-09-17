from django.shortcuts import render, redirect, reverse, get_object_or_404
from . import views
from django.views import generic
from .models import Product, Customer
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import Group

from django.contrib import messages
from django.http import HttpResponseRedirect

from .forms import *

# shwing all the available products

def home(request):
    products = Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'products': products,
        'num_visits' : num_visits
    }
    return render(request, 'home.html', context)

def userSignup(request):
    userForm= CustomerUserCreationForm()
    customerForm=CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=CustomerUserCreationForm(request.POST)
        customerForm=CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return redirect('login')
    return render(request,'registration/signup.html',context=mydict)

def my_cart(request):
    return render(request, 'cart.html')


def add_to_cart(request, pk):
    products = Product.objects.all()
    #for cart counter, fetching products ids added by customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=1
    
    response = render(request, 'home.html',{'products':products,'product_count_in_cart':product_count_in_cart})
    
    #adding product id to cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids=="":
            product_ids=str(pk)
        else:
            product_ids=product_ids+"|"+str(pk)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', pk)

    product=Product.objects.get(id=pk)
    messages.info(request, product.name + ' added to cart successfully!')

    return response

def customer_profile(request, pk):
    if pk:
        queryset = User.objects.get(id=pk)

        form = CustomerForm()
        context = {
                'queryset': queryset,
                'form': form
            }
        return render(request, 'customer_profile.html', context)
    else:
        return render(request, 'customer_profile.html')

class CutomerProfile(generic.TemplateView):
    template_name = 'customer_profile.html'
    form_class = CustomerForm



class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomerUserCreationForm

    def get_success_url(self):
        return reverse("login")
    
class LogoutViewRedirect(LogoutView):
    template_name = "registration/logout.html"

    def get_success_url(self):
        return reverse('shop:home')    


    
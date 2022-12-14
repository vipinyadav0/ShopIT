from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View, generic
import json
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new

import stripe
from django.conf import settings
from . import views
from .forms import *
from .models import Customer, Product, Order, ShippingAddress

# shwing all the available products

class Home(View):
    def get(self, request):
        products = Product.objects.all()
        print("product is: ",products)
        print("request is: ",request)
        print("cookie is:  ",request.COOKIES)
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
        print(request.session.get('cart'))
        print(request.session.get('customer'))


        return render(request, 'home.html', context)

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        request.session.get('cart') == "Cart"
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1

                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
            
        else:
            pass
            cart = {}
            cart[product] = 1
        
        request.session['cart'] = cart

        return redirect('shop:home')

def userSignup(request):
    userForm= CustomerUserCreationForm()
    customerForm=CustomerForm()
    mydict={'userForm':userForm, 'customerForm':customerForm}
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
    if not request.session.get('cart'):
        print("No item in cart")
    else:
        print("cart item is: ",request.session.get('cart'))
        ids = list(request.session.get('cart').keys())
            # print(request.session.get('user'))
        products = Product.get_products_by_id(ids)
        length = len(products)
        context = {
            'products': products,
            'length': length
        }
        return render(request, 'cart.html', context)
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
    
class LogoutViewRedirect(LogoutView):
    template_name = "registration/logout.html"

    def get_success_url(self):
        return reverse('shop:home')    


class Login(LoginView):
    model = User
    template_name = "registration/login.html"

    # accessing user into session to get its data
    def post(self, *args, **kwargs):
        customer = self.request.POST['username']
        user = User.objects.get(username=customer)
        user_id = user.id
        customer = Customer.objects.get(user_id = user_id)
        self.request.session['customer'] = customer.id

        return super().post(*args, **kwargs)

    def get_success_url(self):
        return reverse('shop:home')

def checkout(request):
    # request_data = json.loads(request.body)
    # print("req data us: ", request_data)
    print(request.body)
    print("cart is :", request.session['cart'])
    ca = request.session['cart']
    print(ca)
    sum(ca.values())
    if request.user.is_authenticated:
        print(request.session.get('cart'))
        ids = list(request.session.get('cart').keys())
                # print(request.session.get('user'))
        products = Product.get_products_by_id(ids)
        length = len(products)
        context = {
            'products': products,
            'length': length
        }
        if request.method == "POST":
            f_name = request.POST['First Name']
            address = request.POST['Address']
            phone_number = request.POST['tel']
            city = request.POST['City']
            state = request.POST['State']

            context.update({'address': address,
                            'phone_number':phone_number,
                            'city':city,
                            'state':state
            })

            ShippingAddress.objects.create(first_name=f_name)
            print(context)
            return render(request, 'order_summary.html', context)
        else:
            return render(request, 'checkout.html', context)

    else:
        userForm= CustomerUserCreationForm()
        customerForm=CustomerForm()
        context={'userForm':userForm, 'customerForm':customerForm}
        return render(request, 'registration/signup.html', context)


# class CreateCheckoutSessionview(View):
    # def post(self, request, *args, **kwargs):
    #     YOUR_DOMAIN= "https://127.0.0.8080"
    #     checkout_session = stripe.checkout.Session.create(
    #         line_items=[
    #             {
    #                 # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
    #                 'price': 88800,
    #                 'quantity': 1,
    #             },
    #         ],
    #         mode='payment',
    #         success_url=YOUR_DOMAIN + '/success/',
    #         cancel_url=YOUR_DOMAIN + '/cancel/',
    #     )
    #     return JsonResponse({
    #         'id': checkout_session.id
    #     })
    def create_checkout_session(request, id):

        request_data = json.loads(request.body)
        print("cart is :", request.session['cart'])
        ca = request.session['cart']
        print(ca)
        total = sum(ca.values())

        product = get_object_or_404(Product, pk=id)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            # Customer Email is optional,
            # It is not safe to accept email directly from the client side

            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                        'name': "Products",
                        },
                        'unit_amount': int(product.price * 100),
                    },
                    'quantity': total,
                }
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        return JsonResponse({'sessionId': checkout_session.id})
    
    
# @csrf_exempt
# def stripe_config(request):
#     if request.method == 'GET':
#         stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
#         return JsonResponse(stripe_config, safe=False)

# @csrf_exempt
# def create_checkout_session(request):
#     if request.method == 'GET':
#         domain_url = 'http://localhost:8000/'
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         try:
#             # Create new Checkout Session for the order
#             # Other optional params include:
#             # [billing_address_collection] - to display billing address details on the page
#             # [customer] - if you have an existing Stripe Customer ID
#             # [payment_intent_data] - capture the payment later
#             # [customer_email] - prefill the email input in the form
#             # For full details see https://stripe.com/docs/api/checkout/sessions/create

#             checkout_session = stripe.checkout.Session.create(
#                 success_url=domain_url + '/success/',
#                 cancel_url=domain_url + '/cancel/',
#                 payment_method_types=['card'],
#                 mode='payment',
#                 line_items=[
#                     {
#                         'name': 'T-shirt',
#                         'quantity': 1,
#                         'currency': 'usd',
#                         'amount': '2000',
#                     }
#                 ]
#             )
#         except Exception as e:
#             return JsonResponse({'error': str(e)})


# class OrderSummaryView(generic.TemplateView):
#     template_name = 'order_summary.html'


YOUR_DOMAIN = 'http://localhost:8000'
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_sessionn(request):
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price': "price_1M94ihSD7rISbdVtTgbwr9CO",
                'quantity': 1,
            },  
        ],
        mode='payment',
        success_url=YOUR_DOMAIN + '/success/',
        cancel_url=YOUR_DOMAIN + '/cancel/',
    )
    print("Success", checkout_session)
    return JsonResponse(({'sessionID':checkout_session['id']}))

def order_summary(request):
    return render(request, 'order_summary.html')
# class SuccessView(generic.TemplateView):
#     template_name = "success.html"

# class CancelView(generic.TemplateView):
#     template_name = "cancel.html"
def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')



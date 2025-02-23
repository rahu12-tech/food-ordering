from django.shortcuts import render , redirect,get_object_or_404
from products.models import * 
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages 
from products.models import User 
import razorpay
from products.client import Client
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.http import JsonResponse
api = razorpay.Client(API_KEY=settings.RAZORPAY_API_KEY, 
                      API_SECRET=settings.RAZORPAY_API_SECRET)


@login_required(login_url='/login/')

def home(request):
    products = Product.objects.all()
    context = {'products' : products}
    return render(request, 'home.html' , context)




def index(request):
    
    return render(request, 'index.html' )

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Username or password is incorrect')
    
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    
    return render(request, 'register.html')


@login_required(login_url='/login/')

def add_cart(request, Product_uid):
    Product_obj = Product.objects.get(uid=Product_uid)
    cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
    CartItems.objects.create(cart=cart, product=Product_obj)

    cart_count = CartItems.objects.filter(cart=cart).count()  # Get the updated cart count
    return redirect('/')
@login_required(login_url='/login/')

def cart(request):
    cart = Cart.objects.get(is_paid=False, user=request.user)
    api = Client()  # Initialize the Client object
    response = api.payment_request_create(
        amount=cart.get_cart_total() * 100,  # Amount in paise
        purpose="Order",
        buyer_name=request.user.username,
        email='jakhar365365@gmail.com',  # Single string for email
        redirect_url="http://127.0.0.1:8000/success/"
    )
    order_id = response['id']
    payment_url = f"https://checkout.razorpay.com/v1/checkout.js?order_id={order_id}&key={settings.RAZORPAY_API_KEY}&amount={cart.get_cart_total() * 100}&name={request.user.username}&email=jakhar365365@gmail.com&contact=9999999999&description=Order"

    print(response)
    context = {
        'cart': cart,
        'payment_url': payment_url,
        'razorpay_key': settings.RAZORPAY_API_KEY,  # Pass the Razorpay key
        'order_id': order_id,
        'redirect_url': "http://127.0.0.1:8000/success/"
    }
    return render(request, 'cart.html', context)

@login_required(login_url='/login/')

def remove_cart_item(request , cart_item_uid):
    try:
        CartItems.objects.get(uid = cart_item_uid).delete()
        return redirect('/cart')
    except Exception as e:
        print(e)


@login_required(login_url='/login/')

def orders(request):
    orders = Cart.objects.filter(is_paid = True , user = request.user)
    context = {'orders' : orders}   
    return render(request, 'order.html' , context)


# def create_payment(request):
#     try:
#         email = request.POST.get('email')
#         amount = request.POST.get('amount')  # Collect amount from the front end

#         # Create an order
#         order = client.order.create({
#             'amount': int(amount) * 100,  # Convert to paise
#             'currency': 'INR',
#             'payment_capture': 1,
#             'receipt': 'receipt_order_74394',
#             'notes': {'email': email}
#         })

#         # Pass order_id to the front end for processing the payment
#         return JsonResponse({'order_id': order['id'], 'key': settings.RAZORPAY_API_KEY})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)

# def payment_success(request):
#     return render(request, 'payment_success.html')
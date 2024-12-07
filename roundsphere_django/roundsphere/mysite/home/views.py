from django.shortcuts import render, HttpResponse
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import RegistrationForm
from .utils import email_verification_token
from django.contrib.auth import login
from django.http import HttpResponse


# Create your views here.

def index(request):
    # if request.user.is_anonymous:
    #     return redirect("/login")
    return render(request, 'index.html') 
    
    # return HttpResponse("this is homepage")

def about(request):
    return render(request, 'about.html') 

    # return HttpResponse("this is about page")

def contact(request):
    return render(request, 'contact.html') 

    # return HttpResponse("this is Contact page")

def blog(request):
    return render(request, 'blog.html') 

    
    # return HttpResponse("this is shop page")
    
    
def data(request):
    return render(request, 'data.html') 


def login(request):
    # if request.method== "POST":
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
      #check if user has entered correct credentials
        # user = authenticate(username=username, password=password)
    
        # if user is not None:
        # # A backend authenticated the credentials
        #   return redirect("/")
        # else:
             # No backend authenticated the credentials
            # return render(request, 'login.html') 
    return render(request, 'login.html') 

# def logoutUser(request):
#     logout(request)
#     return redirect("/login")


def shop(request):
    return render(request, 'shop.html') 

def signup(request):
    return render(request, 'signup.html') 



def products_view(request):
    # Fetch all products from the database
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def sendemails(request):
       return render(request, 'login.html') 
   
   
def shopview(request):
    return render(request, 'shop.html') 

# def signup(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # Inactive until email verification
#             user.save()

#             # Send verification email
#             current_site = get_current_site(request)
#             subject = 'Activate Your Account'
#             message = render_to_string('email_verification.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': email_verification_token.make_token(user),
#             })
#             send_mail(
#                 subject,
#                 message,
#                 'your-email@gmail.com',
#                 [user.email],
#                 fail_silently=False,
#             )
#             return render(request, 'email_sent.html', {'email': user.email})
#     else:
#         form = RegistrationForm()
#     return render(request, 'register.html', {'form': form})

# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and email_verification_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return render(request, 'activation_success.html')
#     else:
#         return HttpResponse('Activation link is invalid!')

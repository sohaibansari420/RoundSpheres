from django.shortcuts import render, HttpResponse, redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login as auth_login
from .models import User    
from django.contrib import messages
# from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import RegistrationForm, UserUpdateForm
from .utils import email_verification_token
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.

def index(request):
    # if request.user.is_anonymous:
    #     return redirect("/login")
    return render(request, 'users/index.html') 
    
    # return HttpResponse("this is homepage")

def about(request):
    return render(request, 'users/about.html') 

    # return HttpResponse("this is about page")

def contact(request):
    return render(request, 'users/contact.html') 

    # return HttpResponse("this is Contact page")

def blog(request):
    return render(request, 'users/blog.html') 

    
    # return HttpResponse("this is shop page")
    
    
def data(request):
    return render(request, 'users/data.html') 


def shop(request):
    products = Product.objects.all()
    return render(request, 'users/shop.html', {'products': products}) 


def products_view(request):
    # Fetch all products from the database
    products = Product.objects.all()
    return render(request, 'user/products.html', {'products': products})

def sendemails(request):
       return render(request, 'registration/signup.html') 
   
   
def shopview(request):
    return render(request, 'users/shop.html') 


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            # Save the user but set `is_active` to False
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # Generate the email verification link
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('registration/email_verification.html', {
                'user': user.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            """Send email"""
            email = EmailMessage(
                subject,
                message,
                'primefordfx@gmail.com',  # Replace with your email address
                [user.email],
            )
            email.content_subtype = "html"  # Set content type to HTML
            email.send(fail_silently=False)

            # Redirect to an email-sent confirmation page
            return render(request, 'registration/email_sent.html', {'user': user})
        else:
            print(form.errors)  # Debug: Print form errors in the terminal
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate_account(request, uidb64, token):
    """Activate the user's account if the token is valid."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/account_activated.html', {'user': user})
    else:
        return HttpResponse('Activation link is invalid!', status=400)
    
# def login(request):
#     if request.method== "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#       check if user has entered correct credentials
#         user = authenticate(username=username, password=password)
    
#         if user is not None:
#         # A backend authenticated the credentials
#           return redirect("/")
#         else:
#              No backend authenticated the credentials
#             return render(request, 'login.html') 
#     return render(request, 'login.html') 

# def login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         # Authenticate the user
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             # Log the user in
#             auth_login(request, user)
#             return redirect("home")  # Redirect to a named URL pattern
#         else:
#             # Invalid credentials
#             messages.error(request, "Invalid username or password.")
#             return render(request, 'login.html')
#     else:
#         return render(request, 'login.html')


# def login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         # Check if user has entered correct credentials
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             # A backend authenticated the credentials
#             auth_login(request, user)
#             return redirect("home")  # Redirect to the home page or any other page
#         else:
#             # No backend authenticated the credentials
#             messages.error(request, "Invalid username or password.")
#             return render(request, 'registration/login.html')
#     else:
#         return render(request, 'registration/login.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('update-profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'registration/update_profile.html', {'form': form})

# @login_required
# def logout(request):
#     logout(request)
#     messages.info(request, "You have successfully logged out.")
#     return redirect('users/index.html')  # Redirect to the home page or any other page

# def logoutUser(request):
#     logout(request)
#     return redirect("/login")
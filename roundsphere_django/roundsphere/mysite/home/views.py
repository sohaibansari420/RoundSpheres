from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
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
    return render(request, 'login.html') 


def shop(request):
    return render(request, 'shop.html') 

def signup(request):
    return render(request, 'signup.html') 
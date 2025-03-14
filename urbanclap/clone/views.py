from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.models import *
# Create your views here.

@login_required
def home(request):
    return render(request,'clone/home.html')



@login_required
def service_page(request):
    return render(request,'clone/service.html')

@login_required
def view_category(request):
    data = Category.objects.all()
    sub_data = subcatagory.objects.all()
    services = service.objects.all()
    return render(request, 'clone/wireframe.html',{'data':data,'sub_data':sub_data,'services': services})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email ,password=password)
        user.save()
        login(request,user)
        return redirect('home')
    return render(request,'clone/register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'clone/index.html', {'error_message': 'Invalid login'})
    return render(request,'clone/index.html')

def logout_user(request):
    logout(request)
    return redirect('login_user')

def search_service(request):
    query = request.GET.get('q')  # Get the search term from the URL
    results = []

    if query:
        results = service.objects.filter(name__icontains=query)  # Case-insensitive search

    return render(request, 'clone/search.html', {'results': results, 'query': query})



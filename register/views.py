from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def register(response):
		if response.user.is_authenticated:
			return redirect('products:item_create_url')
		
		else:
			form=RegisterForm()
			if response.method == "POST":
				form = RegisterForm(response.POST)
				if form.is_valid():
					user = form.cleaned_data.get("username")
					form.save()
					messages.success(response,'Account was created for '+ user)
					return redirect("/")
			return render(response, "register/register.html", {"form":form})

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('products:item_create_url')
		
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('products:item_create_url')
			else:
				messages.error(request, 'Username OR password is incorrect')
		return render(request, 'registration/login.html')

def logoutUser(request):
	logout(request)
	return redirect('login')



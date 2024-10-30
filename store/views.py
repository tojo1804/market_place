from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Product,Category,Profile

from django import forms 
from django.db.models import Q
# Create your views here.
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout 
from .forms import SignUpForm,UpdateUserForm,UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress

 
import json
from cart.cart import Cart 
 
def update_info(request):
	if request.user.is_authenticated: 
		current_user=Profile.objects.get(user__id=request.user.id)
		shipping_user=ShippingAddress.objects.get()
		#get orginal userform
		form = UserInfoForm(request.POST or None , instance=current_user)
		#get user's shipping form
		shipping_form =ShippingForm(request.POST or None , instance=shipping_user)
		if form.is_valid():
			form.save() 
			shipping_form.save()
			messages.success(request,' votre info bien modifie')
			return redirect('home')
		return render(request,"update_info.html",{'form':form,'shipping_form':shipping_form,})
	else:
		messages.success(request,"connecter encore pour acceder")
		return redirect('home')


def update_user(request):
	if request.user.is_authenticated:
		current_users=User.objects.get(id=request.user.id)
		user_form =UpdateUserForm(request.POST or None , instance=current_users)
		if user_form.is_valid():
			user_form.save()
			login(request,current_users)
			messages.success(request,'bien modifie')
			return redirect('home')
		return render(request,"update_user.html",{'user_form':user_form})
	else:
		messages.success(request,"connecter encore pour acceder")
		return redirect('home')

def login_user(request):
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			#do something cart shopping
			current_user=Profile.objects.get(user__id=request.user.id)
			#get thier saved cart from database 
			saved_cart=current_user.old_cart
			#canvert database string to python dictionnary
			if saved_cart:

				#convert to dictionnary using json 
				converted_cart=json.loads(saved_cart)
				#add the loaded cart dictionnary  to our session 
				#get the cart 
				cart=Cart(request) 
				#let loop througth the cart and the items from the database
				for key,value in converted_cart.items():
					cart.db_add(product=key,quantity=value)
			messages.success(request,("you have been looged in "))
			return redirect("home")
		else:
			messages.success(request,("there was an error,please try again"))
			return redirect("login")

	else:
		return render(request,'login.html',{})
def logout_user(request):
	# return render(request,'login.html',{})
	logout(request)
	messages.success(request,("you have been loged out"))
	return redirect('home')

 
 
def category_summary(request):
	categories=Category.objects.all()
	return render(request,'category_summary.html',{'categories':categories})
	return redirect('home')
	# messages.success(request,"connecter")
	
def category(request, foo):
	foo=foo.replace('-',' ')
	try:
		category=Category.objects.get(name=foo)
		products=Product.objects.filter(category=category)
		return render(request,'category.html',{'category':category,'products':products})

	except:
		# messages.success(request,("that category doesn't existe"))
		return redirect('home')


def search(request):
	# determine if they fill the form before searching
	if request.method=='POST':
		searched= request.POST['searched']
		#let querry the product 
		searched=Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		#let test for the null ou tsis n 'inonona'
		if not searched:
			# messages.success(request,'sorry that product not exist..........please try again')
			
			return render(request,"search.html",{})
		else:
			return render(request,"search.html",{"searched":searched})

	else:
		return render(request,"search.html",{})
	

def home(request):
	products=Product.objects.all()
	return render(request,'home.html',{"products":products})
def detail(request,pk):
	product=Product.objects.get(id=pk)
	return render(request,'detail.html',{"product":product})

def register_user(request):
	form=SignUpForm()
	if request.method=="POST":
		form=SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data['username']
			password=form.cleaned_data['password1']
			user=authenticate(username=username,password=password)
			login(request,user)
			messages.success(request,("username created- please fill out your user info below"))
			return redirect('login')
		else:
			messages.success(request,("there was en error,try again"))
			return redirect('register')
	else:
		return render(request,'register.html',{"form":form})

def apropos(request):
	return render(request,"apropos.html")
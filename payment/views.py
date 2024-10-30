from django.shortcuts import render,redirect
from cart.cart import Cart
from django.contrib.auth.models import User
from payment.models import ShippingAddress,Order ,OrderItem
from payment.models import *
from store.models import Product , Profile
from payment.forms import ShippingForm,PaymentForm
from django.conf import settings
from django.contrib import messages
import datetime

#some paypal stuff
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid #unique id for duplicate orders


# Create your views here.
def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		#get the order 
		order=Order.objects.get(id=pk)
		#get the order item 
		items=OrderItem.objects.filter(order=pk)
		if request.POST:
			status=request.POST['shipping_status']
			#check if true or false 
			if status=="true":
				order=Order.objects.filter(id=pk)
				#update it
				now=datetime.datetime.now()
				order.update(shipped=True,date_shipped=now)
				return redirect('home')
			else:
				order=Order.objects.filter(id=pk)
				#update it
				order.update(shipped=False)
			messages.success(request,"modifié")
			return redirect('home')
				

		return render(request,"payment/orders.html",{"order":order,"items":items})
		
	else:
		messages.success(request,"tu n est pas un admin")
		return redirect('home')
		
def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders=Order.objects.filter(shipped=False)
		if request.POST:
			status=request.POST['shipping_status']
			num=request.POST['num']
			order=Order.objects.filter(id=num)
			now=datetime.datetime.now()
			order.update(shipped=True,date_shipped=now)

			return redirect('home')

		return render(request,"payment/not_shipped_dash.html",{"orders":orders})
	else:
		messages.success(request,"tu n est pas un admin")
		return redirect('home')
		

def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders=Order.objects.filter(shipped=True)
		if request.POST:
			status=request.POST['shipping_status']
			num=request.POST['num']
			order=Order.objects.filter(id=num)
			now=datetime.datetime.now()
			order.update(shipped=False)
			
			return redirect('home')
		return render(request,"payment/shipped_dash.html",{"orders":orders})
	else:
		messages.success(request,"tu n est pas un admin")
		return redirect('home')
		
	
	


def process_order(request):
	if request.POST:
		cart=Cart(request) 
		cart_products=cart.get_prods
		quantities=cart.get_quants
		totals=cart.cart_total()

		#let get billing info from the last page
		payment_form=PaymentForm(request.POST or None)
		#get the shipping session data 
		my_shipping=request.session.get('my_shipping')
		#gather Order info
		full_name=my_shipping['shipping_full_name']
		email=my_shipping['shipping_full_name']
		#create shipping address from session info
		shipping_address=f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_country']}\n{my_shipping['shipping_country']}"
		amount_paid=totals
		#create an  order 

		if request.user.is_authenticated:
			#login
			user=request.user
			#create order
			create_order=Order(user=user,full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
			create_order.save()
			#add order item
			#let get the order id
			order_id=create_order.pk
			#get the product info
			for product in cart_products():
				#let get the productid
				product_id=product.id
				if product.is_sale:
					price=product.sale_price
				else:
					price=product.price 

				#get quantity
				for key,value in quantities().items():
					if int(key)==product.id:
						#create order item 
						create_order_item=OrderItem(order_id=order_id,product_id=product_id,user=user,quantity=value,price=price)
						create_order_item.save()
			#delete our cart 
			for key in list(request.session.keys()):
				if key=="session_key":
					#delete the key
					del request.session[key]
			#delete our cart  from database (old cart field)

			current_user=Profile.objects.filter(user__id=request.user.id)
			#delete shopping cart ind database(old cart field)
			current_user.update(old_cart="")




			return redirect('home')
		else:

			#not login
			#create order
			create_order=Order(full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
			create_order.save()

			#add order item
			#let get the order id
			order_id=create_order.pk
			#get the product info
			for product in cart_products():
				#let get the productid
				product_id=product.id
				if product.is_sale:
					price=product.sale_price
				else:
					price=product.price 

				#get quantity
				for key,value in quantities().items():
					if int(key)==product.id:
						#create order item 
						create_order_item=OrderItem(order_id=order_id,product_id=product_id,quantity=value,price=price)
						create_order_item.save()
			#delete our cart 
			for key in list(request.session.keys()):
				if key=="session_key":
					#delete the key
					del request.session[key]






			return redirect('home')

	else:

		return render(request,"payment/process_order.html")
	 









def payment_success(request):
	return render(request,'payment/payment_success.html',{})
def payment_failed(request):
	return render(request,'payment/payment_failed.html',{})
def checkout(request): 
	# get the cart 
	cart=Cart(request) 
	cart_products=cart.get_prods
	quantities=cart.get_quants
	totals=cart.cart_total()
	if request.user.is_authenticated:
		shipping_user=ShippingAddress.objects.get()
	# 	#check out as loged in
		shipping_form =ShippingForm(request.POST or None , instance=shipping_user)
		return render(request,"payment/checkout.html",{'cart_products':cart_products,'quantities':quantities, 'totals':totals,'shipping_form':shipping_form})
	else:
	# 	#check ou as guest
		shipping_form =ShippingForm(request.POST or None , instance=shipping_user)
		return render(request,"payment/checkout.html",{'cart_products':cart_products,'quantities':quantities, 'totals':totals,'shipping_form':shipping_form})
	# 	messages.success(request,"access denied, se connecter ")
		# return redirect('home')
	# return render(request,"payment/checkout.html",{}) 

def billing_info(request):
	if request.POST:
		# get the cart 
		cart=Cart(request) 
		cart_products=cart.get_prods
		quantities=cart.get_quants
		totals=cart.cart_total()

		#create a session with shipping info
		my_shipping=request.POST
		request.session['my_shipping']=my_shipping

		#create a paypal form 
		host=request.get_host()
		paypal_dict={
			'business':settings.PAYPAL_RECEIVER_EMAIL,
			'amount':totals,
			'item_name':"Book Order",
			'no_shipping':'2', 
			'invoice':str(uuid.uuid4()),
			'currency_code':'ARIARY',
			'notify_url':'https://{}{}'.format(host,reverse('paypal-ipn')),
			'return_url':'https://{}{}'.format(host,reverse('payment_success')),
			'cancel_return':'https://{}{}'.format(host,reverse('payment_failed')),

 
		}
		#create paypal fomr
		paypal_form=PayPalPaymentsForm(initial=paypal_dict)

		if request.user.is_authenticated:
			billing_form=PaymentForm()
			return render(request,"payment/billing_info.html",{"paypal_form":paypal_form,"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_info":request.POST,"billing_form":billing_form})
		else:
			billing_form=PaymentForm()
			return render(request,"payment/billing_info.html",{"paypal_form":paypal_form,"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_info":request.POST,"billing_form":billing_form})

		shipping_info=request.POST
		request.session['shipping_info']=shipping_info
		return render(request,"payment/billing_info.html",{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_info":shipping_info})
	else:
		return redirect('home')
		# return render(request,"payment/billing_info.html",{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_info":shipping_info}) 


	
 
	
 
# Create your views here.
from django.shortcuts import render,get_object_or_404 , redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages




def cart_summary(request):
	# get the cart 
	if request.user.is_authenticated:
		cart=Cart(request)
		cart_products=cart.get_prods
		quantities=cart.get_quants
		totals=cart.cart_total()
		return render(request,'cart_summary.html',{'cart_products':cart_products,'quantities':quantities,'totals':totals})
	else:
		messages.success(request,"il faut connect avant ")
		return redirect('home')
		



def cart_add(request):
	# get the cart
	cart=Cart(request)
	#let tste the post 
	if request.POST.get('action')== 'post':
		product_id=int(request.POST.get('product_id'))
		product_qty=int(request.POST.get('product_qty'))
		#look up product in DB
		product=get_object_or_404(Product,id=product_id)
		#save to session 
		cart.add(product=product,quantity=product_qty)
		# cart.add(product=product)

		#get cart quantity
		cart_quantity = cart.__len__()
		# response=JsonResponse({'product name:':product.name})
		response = JsonResponse({'qty':cart_quantity})
		# messages.success(request,"produit ajouté dans  la carte...")
		return  response
		
def cart_delete(request):
	cart=Cart(request)
	if request.POST.get('action')== 'post':
		product_id=int(request.POST.get('product_id'))
		# let call delete function
		cart.delete(product=product_id)
		response= JsonResponse({'product':product_id})
		# messages.success(request,"produit supprimé ...")
		return response
	
def cart_update(request):
	cart=Cart(request)
	if request.POST.get('action')== 'post':
		product_id=int(request.POST.get('product_id'))
		product_qty=int(request.POST.get('product_qty'))
		cart.update(product=product_id,quantity=product_qty)

		response= JsonResponse({'qty':product_qty})
		# messages.success(request,"produit ajouté et a jour...")
		return response
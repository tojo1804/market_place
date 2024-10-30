from .cart import Cart 
# create context processor so our cart work
def cart(request):
	return {'cart':Cart(request)}
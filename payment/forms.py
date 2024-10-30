from django import forms
from .models import ShippingAddress



 
class ShippingForm(forms.ModelForm):
	# phone=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'phone'}),required=True)
	shipping_full_name=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Full Name'}),required=True)
	shipping_email=forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}),required=True)
	shipping_address1=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address1'}),required=True)
	shipping_country=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Country'}),required=True)
	shipping_telephone=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'telephone'}),required=True)

	class Meta:
		model=ShippingAddress
		fields=['shipping_full_name','shipping_email','shipping_address1','shipping_country','shipping_telephone']
		exclude=['user',]


class PaymentForm(forms.Form):
	cart_name=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name on cart'}),required=False)
	cart_number=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Cart Number'}),required=False)
	cart_exp_date=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Expiration date'}),required=True)
	cart_address1=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'billing Address1'}),required=True)
	cart_city=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'billing City'}),required=True)
	cart_state=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'billing State'}),required=True)
	cart_zipcode=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'billing Zipecode'}),required=True)
	cart_country=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'billing country'}),required=True)

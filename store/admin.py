from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Custommer)
admin.site.register(Order)
admin.site.register(Profile)


#mix profile info and user info
class ProfileInline(admin.StackedInline):
	model=Profile
#extend the user models
class UserAdmin(admin.ModelAdmin):
	model=User
	field=["username","first_name","last_name","email"]
	inlines=[ProfileInline]
#unregister thee old way 
admin.site.unregister(User)
# re-register the new way
admin.site.register(User,UserAdmin)
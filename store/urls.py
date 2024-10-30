
from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name="home"),
    path('detail/<int:pk>',views.detail,name="detail"),
    path('search/',views.search,name="search"),
    path('category/<str:foo>',views.category,name="category"),
    path('category_summary/',views.category_summary,name='category_summary'),
    path('register',views.register_user,name='register'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('update_user/',views.update_user,name='update_user'),
    path('update_info/',views.update_info,name='update_info'),
    path('apropos/',views.apropos,name='apropos'),
]

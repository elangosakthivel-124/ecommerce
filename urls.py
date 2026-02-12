from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product'),
    path('add/<int:id>/', views.add_to_cart, name='add'),
    path('cart/', views.cart, name='cart'),
    path('remove/<int:id>/', views.remove_cart, name='remove'),

    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('addqty/<int:id>/', views.add_qty, name='addqty'),
    path('subqty/<int:id>/', views.sub_qty, name='subqty'),
    path('checkout/', views.checkout, name='checkout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('order/<int:id>/', views.order_detail, name='order_detail'),


]

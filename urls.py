from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('register/',views.register_user,name='register'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('add/<int:id>/',views.add_to_cart),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout),
    path('payment/<int:id>/',views.payment,name='payment'),
    path('success/<int:id>/',views.success),
    path('dashboard/',views.dashboard),
]

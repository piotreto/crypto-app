from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('sell/<slug:id>/<slug:amount>/', views.sell, name='sell'),
    path('buy/<slug:id>/<slug:amount>/', views.buy, name='buy'),
    path('wallet_details/', views.wallet_details, name="wallet_details")
]
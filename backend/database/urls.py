from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('sell/<slug:id>/<slug:amount>/', views.sell, name='sell'),
    path('buy/<slug:id>/<slug:amount>/', views.buy, name='buy'),
    path('wallet_details/', views.wallet_details, name="wallet_details"),
    path('trade_history/', views.trades_history, name="trade_history"),
    path('daily_statistics/', views.daily_statistics, name="daily_statistics"),
    path('daily_crypto_statistics/', views.daily_crypto_statistics, name="daily_crypto_statistics")
]
from django.urls import path
from . import views

urlpatterns = [
    path('<slug:id>/<slug:vs_currency>/<slug:days>/<slug:interval>', views.plot, name='plot-home'),
    path('<slug:id>/<slug:vs_currency>/<slug:days>', views.plot_no_interval, name='plot-no-interval'),
    path('list', views.cryptoList, name='crypto-list'),
]

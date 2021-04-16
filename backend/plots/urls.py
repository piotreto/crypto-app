from django.urls import path
from . import views

urlpatterns = [
    path('<slug:id>/<slug:vs_currency>/<slug:days>/<slug:interval>', views.plot, name='plot-home')
]

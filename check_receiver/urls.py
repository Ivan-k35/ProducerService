from django.urls import path

from . import views

app_name = 'check_receiver'

urlpatterns = [
    path('checks/', views.PurchaseCheckView.as_view(), name='receive_purchase_check'),
]

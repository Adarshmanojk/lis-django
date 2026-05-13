from django.urls import path
from .views import OrderListCreateView, OrderDetailView, CollectOrderView, ReceiveOrderView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/collect/', CollectOrderView.as_view(), name='order-collect'),
    path('orders/<int:pk>/receive/', ReceiveOrderView.as_view(), name='order-receive'),
]

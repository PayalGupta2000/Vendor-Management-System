from django.urls import path
from . views import *

urlpatterns = [
    path('login/',LoginAPI.as_view(),name='login'),
    path('vendors/',VenorAPIView.as_view(),name='vendor-list'),
    path('purchase_orders/',PurchaseOrderAPIView.as_view(),name='purchase-order-list'),
    path('vendors/',vendorPerformanceAPIView.as_view(),name='vendor-performance'),
    path('filter-purchase-order-by-vendor/',FilterPurchaseOrderAPIView.as_view()),
]

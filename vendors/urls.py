from django.urls import path
from . views import *

urlpatterns = [
    path('vendors/',VenorListView.as_view(),name='vendor-list'),
    path('vendors/<int:vendor_id>/',VendorDetailView.as_view(),name='vendor-detail'),
    path('purchase_orders/',PurchaseOrderListView.as_view(),name='purchase-order-list'),
    path('purchase_orders/<int:po_id>/',PurchaseOrderListView.as_view(),name='purchase-order-detail'),
    path('vendors/<int:vendor_id>/performance/',vendorPerformanceView.as_view(),name='vendor-performance'),
]

# In vendor_management/urls.py

from django.urls import path
from . import api

urlpatterns = [
    # Vendor endpoints
    path('vendors/', api.create_vendor, name='create_vendor'),
    path('vendors/', api.list_vendors, name='list_vendors'),
    path('vendors/<int:vendor_id>/', api.retrieve_vendor, name='retrieve_vendor'),
    path('vendors/<int:vendor_id>/', api.update_vendor, name='update_vendor'),
    path('vendors/<int:vendor_id>/', api.delete_vendor, name='delete_vendor'),

    # Purchase order endpoints
    path('purchase_orders/', api.create_purchase_order, name='create_purchase_order'),
    path('purchase_orders/', api.list_purchase_orders, name='list_purchase_orders'),
    path('purchase_orders/<int:po_id>/', api.retrieve_purchase_order, name='retrieve_purchase_order'),
    path('purchase_orders/<int:po_id>/', api.update_purchase_order, name='update_purchase_order'),
    path('purchase_orders/<int:po_id>/', api.delete_purchase_order, name='delete_purchase_order'),

    # Vendor performance endpoint
    path('vendors/<int:vendor_id>/performance/', api.vendor_performance, name='vendor_performance'),

    # Acknowledge purchase order endpoint
    path('purchase_orders/<int:po_id>/acknowledge/', api.acknowledge_purchase_order, name='acknowledge_purchase_order'),
]

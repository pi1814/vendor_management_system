from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor, PurchaseOrder

class VendorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_vendor(self):
        url = reverse('create_vendor')
        data = {'name': 'Test Vendor', 'contact_details': 'test@example.com', 'address': '123 Test St', 'vendor_code': 'TEST123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.get().name, 'Test Vendor')

    def test_list_vendors(self):
        url = reverse('list_vendors')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_vendor(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com', address='123 Test St', vendor_code='TEST123')
        url = reverse('retrieve_vendor', kwargs={'vendor_id': vendor.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Vendor')

    # Implement test cases for update_vendor and delete_vendor similarly

class PurchaseOrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_purchase_order(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com', address='123 Test St', vendor_code='TEST123')
        url = reverse('create_purchase_order')
        data = {'po_number': 'PO123', 'vendor': vendor.id, 'order_date': '2022-05-07T12:00:00Z', 'delivery_date': '2022-05-14T12:00:00Z', 'items': [], 'quantity': 10, 'status': 'pending'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)
        self.assertEqual(PurchaseOrder.objects.get().po_number, 'PO123')

    # Implement test cases for list_purchase_orders, retrieve_purchase_order, update_purchase_order, delete_purchase_order similarly

    def test_acknowledge_purchase_order(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com', address='123 Test St', vendor_code='TEST123')
        purchase_order = PurchaseOrder.objects.create(po_number='PO123', vendor=vendor, order_date='2022-05-07T12:00:00Z', delivery_date='2022-05-14T12:00:00Z', items=[], quantity=10, status='pending')
        url = reverse('acknowledge_purchase_order', kwargs={'po_id': purchase_order.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(PurchaseOrder.objects.get(id=purchase_order.id).acknowledgment_date)

    # Implement test cases for vendor_performance similarly


from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer


class OrderListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin = User.objects.create_superuser(username='adminuser', password='adminpass')
        self.order1 = Order.objects.create(user=self.user, name='Order 1', total=10)
        self.order2 = Order.objects.create(user=self.user, name='Order 2', total=20)
        self.order3 = Order.objects.create(user=self.admin, name='Order 3', total=30)

    def test_order_list_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = OrderSerializer([self.order1, self.order2], many=True).data
        self.assertEqual(response.data, serializer_data)

    def test_order_list_superuser(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = OrderSerializer([self.order1, self.order2, self.order3], many=True).data
        self.assertEqual(response.data, serializer_data)

    def test_create_order(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('order-list')
        data = {
            'name': 'Order 4',
            'total': 40
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(name='Order 4')
        serializer_data = OrderSerializer(order).data
        self.assertEqual(response.data, serializer_data)

    def test_create_order_with_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('order-list')
        data = {
            'name': 'Order 5'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

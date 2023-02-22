from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class OrderList(APIView):
    
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        if request.user.is_superuser:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
        
        orders = Order.objects.filter(user_id=request.user.id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, request):
        try:
            if request.user.is_superuser:
                return Order.objects.get(pk=pk)
            return Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            raise Http404("Order not found")
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        order = self.get_object(pk, request)
        if isinstance(order, Response):
            return order
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        order = self.get_object(pk, request)
        if isinstance(order, Response):
            return order

        # Make the user field read-only
        request.data['user'] = order.user.id
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk, request)
        if isinstance(order, Response):
            return order
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            return super().put(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderListByUserEmail(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        emails = request.query_params.get('email')
        if not emails:
            return Response({'error': 'email parameter is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Get orders owned by users with specified email addresses
        orders = Order.objects.filter(user__email__in=emails.replace(' ', '').split(','))
        # Serialize orders and return as response
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class UserEmailsList(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # Get all email addresses of all users
        emails = User.objects.values_list('email', flat=True)
        
        # Return email addresses as response
        return Response(emails)
    
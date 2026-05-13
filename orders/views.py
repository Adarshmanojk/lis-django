from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import OrderTransaction
from .serializers import OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer
from accounts.permissions import IsAdminOrPhysicianOrNurse, IsPhlebotomist, IsLabTechnician


class OrderListCreateView(generics.ListCreateAPIView):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['order_no', 'patient__mrn', 'patient__patient_name']
    ordering_fields = ['ordered_at', 'order_status']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminOrPhysicianOrNurse()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = OrderTransaction.objects.select_related('patient', 'ordered_by').prefetch_related('lines')
        status_param = self.request.query_params.get('status')
        patient_param = self.request.query_params.get('patient')
        date_param = self.request.query_params.get('date')
        if status_param:
            qs = qs.filter(order_status=status_param)
        if patient_param:
            qs = qs.filter(patient_id=patient_param)
        if date_param:
            qs = qs.filter(ordered_at__date=date_param)
        return qs


class OrderDetailView(generics.RetrieveAPIView):
    queryset = OrderTransaction.objects.prefetch_related('lines__assay', 'results')
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]


class CollectOrderView(APIView):
    permission_classes = [IsAuthenticated, IsPhlebotomist]

    def patch(self, request, pk):
        try:
            order = OrderTransaction.objects.get(pk=pk)
        except OrderTransaction.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        if order.order_status != 1:
            return Response(
                {'error': 'Only Ordered status can be advanced to Collected.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.order_status = 2
        order.collected_by = request.user.profile
        order.collected_at = timezone.now()
        order.save()
        return Response({'message': 'Sample collected successfully.', 'order_no': order.order_no})


class ReceiveOrderView(APIView):
    permission_classes = [IsAuthenticated, IsLabTechnician]

    def patch(self, request, pk):
        try:
            order = OrderTransaction.objects.get(pk=pk)
        except OrderTransaction.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        if order.order_status != 2:
            return Response(
                {'error': 'Only Collected orders can be moved to In-Lab.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.order_status = 3
        order.received_by = request.user.profile
        order.received_at = timezone.now()
        order.save()
        return Response({'message': 'Order received in lab.', 'order_no': order.order_no})

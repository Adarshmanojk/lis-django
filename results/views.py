from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from orders.models import OrderTransaction
from .models import Result
from .serializers import ResultSerializer
from accounts.permissions import IsLabTechnician, IsPhysicianOrNurse


class ResultEntryView(APIView):
    permission_classes = [IsAuthenticated, IsLabTechnician]

    def post(self, request, pk):
        try:
            order = OrderTransaction.objects.prefetch_related('lines').get(pk=pk)
        except OrderTransaction.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        if order.order_status not in (3, 4):
            return Response(
                {'error': 'Results cannot be entered until the sample has reached In-Lab status.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results_data = request.data.get('results', [])
        profile = request.user.profile
        created = []

        for item in results_data:
            assay_id = item.get('assay')
            result, _ = Result.objects.update_or_create(
                order=order,
                assay_id=assay_id,
                defaults={
                    'result_value': item.get('result_value', ''),
                    'unit': item.get('unit', ''),
                    'normal_range': item.get('normal_range', ''),
                    'flag': item.get('flag', ''),
                    'remarks': item.get('remarks', ''),
                    'entered_by': profile,
                }
            )
            created.append(result.id)

        order.order_status = 4
        order.save()

        return Response({'message': 'Results saved. Order marked Completed.', 'result_ids': created})


class LabReportView(APIView):
    permission_classes = [IsAuthenticated, IsPhysicianOrNurse]

    def get(self, request, pk):
        try:
            order = OrderTransaction.objects.select_related(
                'patient', 'ordered_by', 'collected_by', 'received_by'
            ).prefetch_related('results__assay', 'lines__assay').get(pk=pk)
        except OrderTransaction.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        if order.order_status != 4:
            return Response(
                {'error': 'Report is not available. The order must be Completed before the report can be viewed.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = ResultSerializer(order.results.all(), many=True).data
        report = {
            'order_no': order.order_no,
            'ordered_at': order.ordered_at,
            'patient': {
                'mrn': order.patient.mrn,
                'name': order.patient.patient_name,
                'age': order.patient.age,
                'gender': order.patient.gender,
            },
            'ordered_by': order.ordered_by.full_name,
            'collected_by': order.collected_by.full_name if order.collected_by else None,
            'collected_at': order.collected_at,
            'received_by': order.received_by.full_name if order.received_by else None,
            'received_at': order.received_at,
            'results': results,
        }
        return Response(report)

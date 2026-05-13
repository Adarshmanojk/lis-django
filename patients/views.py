from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import PatientMaster
from .serializers import PatientSerializer
from accounts.permissions import IsAdminOrPhysicianOrNurse


class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsAdminOrPhysicianOrNurse]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['mrn', 'patient_name', 'phone']
    ordering_fields = ['created_at', 'patient_name']

    def get_queryset(self):
        return PatientMaster.objects.all()

    def perform_create(self, serializer):
        mrn = self.request.data.get('mrn') or PatientMaster.generate_mrn()
        serializer.save(mrn=mrn)


class PatientDetailView(generics.RetrieveUpdateAPIView):
    queryset = PatientMaster.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsAdminOrPhysicianOrNurse]


class GenerateMRNView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrPhysicianOrNurse]

    def get(self, request):
        return Response({'mrn': PatientMaster.generate_mrn()})

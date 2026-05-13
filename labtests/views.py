from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from .models import TestMenuMaster, AssayMaster
from .serializers import TestMenuSerializer, AssaySerializer
from accounts.permissions import IsAdmin


class TestMenuListCreateView(generics.ListCreateAPIView):
    queryset = TestMenuMaster.objects.all()
    serializer_class = TestMenuSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]


class TestMenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestMenuMaster.objects.all()
    serializer_class = TestMenuSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class AssayListCreateView(generics.ListCreateAPIView):
    serializer_class = AssaySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['assay_code', 'assay_name']

    def get_queryset(self):
        qs = AssayMaster.objects.select_related('menu').all()
        menu_id = self.request.query_params.get('menu')
        if menu_id:
            qs = qs.filter(menu_id=menu_id)
        status = self.request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]


class AssayDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AssayMaster.objects.all()
    serializer_class = AssaySerializer
    permission_classes = [IsAuthenticated, IsAdmin]

from django.urls import path
from .views import PatientListCreateView, PatientDetailView, GenerateMRNView

urlpatterns = [
    path('patients/', PatientListCreateView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('patients/generate-mrn/', GenerateMRNView.as_view(), name='generate-mrn'),
]

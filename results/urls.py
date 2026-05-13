from django.urls import path
from .views import ResultEntryView, LabReportView

urlpatterns = [
    path('orders/<int:pk>/results/', ResultEntryView.as_view(), name='result-entry'),
    path('orders/<int:pk>/report/', LabReportView.as_view(), name='lab-report-api'),
]

"""
Frontend URL routing — maps HTML template views to URL paths.
"""
from django.urls import path
from . import frontend_views

urlpatterns = [
    path('', frontend_views.dashboard, name='dashboard'),
    path('login/', frontend_views.login_view, name='login'),
    path('logout/', frontend_views.logout_view, name='logout'),
    path('ajax/generate-mrn/', frontend_views.generate_mrn_ajax, name='generate_mrn_ajax'),
    path('patients/', frontend_views.patient_list, name='patient_list'),
    path('patients/register/', frontend_views.patient_register, name='patient_register'),
    path('patients/<int:pk>/edit/', frontend_views.patient_edit, name='patient_edit'),
    path('orders/', frontend_views.order_list, name='order_list'),
    path('orders/new/', frontend_views.order_entry, name='order_entry'),
    path('worklist/phlebotomist/', frontend_views.phlebotomist_worklist, name='phlebotomist_worklist'),
    path('worklist/technician/', frontend_views.technician_worklist, name='technician_worklist'),
    path('orders/<int:pk>/report/', frontend_views.lab_report, name='lab_report'),
    path('management/tests/', frontend_views.test_management, name='test_management'),
    path('management/users/', frontend_views.user_management, name='user_management'),
]

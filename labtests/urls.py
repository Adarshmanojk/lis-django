from django.urls import path
from .views import TestMenuListCreateView, TestMenuDetailView, AssayListCreateView, AssayDetailView

urlpatterns = [
    path('tests/menus/', TestMenuListCreateView.as_view(), name='menu-list'),
    path('tests/menus/<int:pk>/', TestMenuDetailView.as_view(), name='menu-detail'),
    path('tests/assays/', AssayListCreateView.as_view(), name='assay-list'),
    path('tests/assays/<int:pk>/', AssayDetailView.as_view(), name='assay-detail'),
]

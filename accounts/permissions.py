"""
Custom DRF permission classes for role-based access control.
Each class checks the authenticated user's role against allowed roles.
"""
from rest_framework.permissions import BasePermission


def get_role(request):
    try:
        return request.user.profile.role
    except Exception:
        return None


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return get_role(request) == 'Admin'


class IsAdminOrPhysicianOrNurse(BasePermission):
    def has_permission(self, request, view):
        return get_role(request) in ('Admin', 'Physician', 'Nurse')


class IsPhlebotomist(BasePermission):
    def has_permission(self, request, view):
        return get_role(request) in ('Admin', 'Phlebotomist')


class IsLabTechnician(BasePermission):
    def has_permission(self, request, view):
        return get_role(request) in ('Admin', 'LabTechnician')


class IsPhysicianOrNurse(BasePermission):
    def has_permission(self, request, view):
        return get_role(request) in ('Admin', 'Physician', 'Nurse')

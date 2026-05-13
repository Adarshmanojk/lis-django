"""
Accounts app models.

UserProfile extends Django's built-in User with LIS-specific fields.
UserAccessMaster stores role-based permissions for each module.
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Physician', 'Physician'),
        ('Nurse', 'Nurse'),
        ('Phlebotomist', 'Phlebotomist'),
        ('LabTechnician', 'Lab Technician'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Locked', 'Locked'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    employee_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    designation = models.CharField(max_length=80)
    department = models.CharField(max_length=80, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_master'
        verbose_name = 'User Profile'

    def __str__(self):
        return f"{self.full_name} ({self.role})"


class UserAccessMaster(models.Model):
    role_name = models.CharField(max_length=50)
    module_name = models.CharField(max_length=80)
    can_view = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_access_master'
        unique_together = ('role_name', 'module_name')

    def __str__(self):
        return f"{self.role_name} → {self.module_name}"

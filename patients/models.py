"""
Patients app models.
"""
from django.db import models


class PatientMaster(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    STATUS_CHOICES = [('Active', 'Active'), ('Inactive', 'Inactive')]

    mrn = models.CharField(max_length=20, unique=True)
    patient_name = models.CharField(max_length=150)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=80)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patient_master'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.mrn} — {self.patient_name}"

    @classmethod
    def generate_mrn(cls):
        last = cls.objects.filter(mrn__startswith='PAT-').order_by('-mrn').first()
        if last:
            try:
                num = int(last.mrn.split('-')[1]) + 1
            except (IndexError, ValueError):
                num = 1
        else:
            num = 1
        return f"PAT-{num:06d}"

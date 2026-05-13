from django.db import models


class TestMenuMaster(models.Model):
    DEPARTMENT_CHOICES = [
        ('Serology', 'Serology'),
        ('Haematology', 'Haematology'),
        ('Biochemistry', 'Biochemistry'),
        ('Microbiology', 'Microbiology'),
        ('Immunology', 'Immunology'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [('Active', 'Active'), ('Inactive', 'Inactive')]

    menu_code = models.CharField(max_length=20, unique=True)
    menu_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'test_menu_master'

    def __str__(self):
        return f"{self.menu_code} — {self.menu_name}"


class AssayMaster(models.Model):
    STATUS_CHOICES = [('Active', 'Active'), ('Inactive', 'Inactive')]

    menu = models.ForeignKey(TestMenuMaster, on_delete=models.PROTECT, related_name='assays')
    assay_code = models.CharField(max_length=20, unique=True)
    assay_name = models.CharField(max_length=150)
    sample_type = models.CharField(max_length=50)
    tat_hours = models.PositiveSmallIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    normal_range = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assay_master'

    def __str__(self):
        return f"{self.assay_code} — {self.assay_name}"

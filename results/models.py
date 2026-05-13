from django.db import models
from orders.models import OrderTransaction
from labtests.models import AssayMaster
from accounts.models import UserProfile


class Result(models.Model):
    FLAG_CHOICES = [
        ('H', 'High'),
        ('L', 'Low'),
        ('CR', 'Critical'),
        ('N', 'Normal'),
    ]

    order = models.ForeignKey(OrderTransaction, on_delete=models.CASCADE, related_name='results')
    assay = models.ForeignKey(AssayMaster, on_delete=models.PROTECT)
    result_value = models.CharField(max_length=200)
    unit = models.CharField(max_length=40, null=True, blank=True)
    normal_range = models.CharField(max_length=100, null=True, blank=True)
    flag = models.CharField(max_length=10, choices=FLAG_CHOICES, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    entered_by = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name='results_entered')
    entered_at = models.DateTimeField(auto_now_add=True)
    verified_by = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='results_verified'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'results'
        unique_together = ('order', 'assay')

    def __str__(self):
        return f"{self.order.order_no} — {self.assay.assay_code}: {self.result_value}"

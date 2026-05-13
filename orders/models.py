from django.db import models
from django.utils import timezone
from patients.models import PatientMaster
from labtests.models import AssayMaster
from accounts.models import UserProfile


class OrderTransaction(models.Model):
    STATUS_CHOICES = [
        (1, 'Ordered'),
        (2, 'Collected'),
        (3, 'In-Lab'),
        (4, 'Completed'),
    ]

    order_no = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(PatientMaster, on_delete=models.PROTECT, related_name='orders')
    ordered_by = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name='orders_placed')
    ordered_at = models.DateTimeField(default=timezone.now)
    collected_by = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders_collected'
    )
    collected_at = models.DateTimeField(null=True, blank=True)
    received_by = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders_received'
    )
    received_at = models.DateTimeField(null=True, blank=True)
    order_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    notes = models.TextField(null=True, blank=True)
    assays = models.ManyToManyField(AssayMaster, through='OrderLine', related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_transaction'
        ordering = ['-ordered_at']

    def __str__(self):
        return f"{self.order_no} — {self.patient.patient_name}"

    @classmethod
    def generate_order_no(cls):
        from django.utils.timezone import now
        year = now().year
        prefix = f"ORD-{year}"
        last = cls.objects.filter(order_no__startswith=prefix).order_by('-order_no').first()
        if last:
            try:
                seq = int(last.order_no[-4:]) + 1
            except ValueError:
                seq = 1
        else:
            seq = 1
        return f"{prefix}{seq:04d}"


class OrderLine(models.Model):
    order = models.ForeignKey(OrderTransaction, on_delete=models.CASCADE, related_name='lines')
    assay = models.ForeignKey(AssayMaster, on_delete=models.PROTECT)

    class Meta:
        db_table = 'order_line'
        unique_together = ('order', 'assay')

    def __str__(self):
        return f"{self.order.order_no} — {self.assay.assay_code}"

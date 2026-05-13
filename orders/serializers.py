from rest_framework import serializers
from .models import OrderTransaction, OrderLine
from patients.serializers import PatientSerializer
from labtests.serializers import AssaySerializer


class OrderLineSerializer(serializers.ModelSerializer):
    assay_detail = AssaySerializer(source='assay', read_only=True)

    class Meta:
        model = OrderLine
        fields = ['id', 'assay', 'assay_detail']


class OrderListSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.patient_name', read_only=True)
    patient_mrn = serializers.CharField(source='patient.mrn', read_only=True)
    test_count = serializers.SerializerMethodField()
    status_label = serializers.CharField(source='get_order_status_display', read_only=True)

    class Meta:
        model = OrderTransaction
        fields = [
            'id', 'order_no', 'patient', 'patient_name', 'patient_mrn',
            'test_count', 'ordered_at', 'order_status', 'status_label',
        ]

    def get_test_count(self, obj):
        return obj.lines.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source='patient', read_only=True)
    lines = OrderLineSerializer(many=True, read_only=True)
    ordered_by_name = serializers.CharField(source='ordered_by.full_name', read_only=True)
    collected_by_name = serializers.CharField(source='collected_by.full_name', read_only=True, allow_null=True)
    received_by_name = serializers.CharField(source='received_by.full_name', read_only=True, allow_null=True)
    status_label = serializers.CharField(source='get_order_status_display', read_only=True)

    class Meta:
        model = OrderTransaction
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    assay_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        min_length=1,
        error_messages={'min_length': 'At least one assay must be added to the order.'}
    )

    class Meta:
        model = OrderTransaction
        fields = ['patient', 'notes', 'assay_ids']

    def create(self, validated_data):
        assay_ids = validated_data.pop('assay_ids')
        user_profile = self.context['request'].user.profile
        order = OrderTransaction.objects.create(
            order_no=OrderTransaction.generate_order_no(),
            ordered_by=user_profile,
            **validated_data,
        )
        for assay_id in assay_ids:
            OrderLine.objects.create(order=order, assay_id=assay_id)
        return order

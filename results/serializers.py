from rest_framework import serializers
from .models import Result
from labtests.serializers import AssaySerializer


class ResultSerializer(serializers.ModelSerializer):
    assay_detail = AssaySerializer(source='assay', read_only=True)
    entered_by_name = serializers.CharField(source='entered_by.full_name', read_only=True)

    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = ['entered_by', 'entered_at', 'created_at', 'updated_at']


class ResultBulkSerializer(serializers.Serializer):
    results = ResultSerializer(many=True)

    def validate(self, data):
        order = self.context['order']
        if order.order_status not in (3, 4):
            raise serializers.ValidationError(
                "Results cannot be entered until the sample has reached In-Lab status."
            )
        return data

from rest_framework import serializers
from .models import PatientMaster


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientMaster
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_age(self, value):
        if not (0 <= value <= 150):
            raise serializers.ValidationError("Age must be a whole number between 0 and 150.")
        return value

    def validate_mrn(self, value):
        qs = PatientMaster.objects.filter(mrn=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("MRN already exists. Please enter a unique Medical Record Number.")
        return value

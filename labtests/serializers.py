from rest_framework import serializers
from .models import TestMenuMaster, AssayMaster


class TestMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestMenuMaster
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class AssaySerializer(serializers.ModelSerializer):
    menu_name = serializers.CharField(source='menu.menu_name', read_only=True)

    class Meta:
        model = AssayMaster
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_assay_code(self, value):
        qs = AssayMaster.objects.filter(assay_code=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Test Code already exists. Please enter a unique code.")
        return value

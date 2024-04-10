from rest_framework import serializers
from .models import inventory_History

class InventoryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = inventory_History
        fields = '__all__'
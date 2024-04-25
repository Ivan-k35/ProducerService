from rest_framework import serializers
from .models import PurchaseCheck, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['purchase_check']


class PurchaseCheckSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, required=False)

    class Meta:
        model = PurchaseCheck
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase_check = PurchaseCheck.objects.create(**validated_data)

        for item_data in items_data:
            Item.objects.create(purchase_check=purchase_check, **item_data)

        return purchase_check

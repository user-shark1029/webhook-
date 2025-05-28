from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import PaymentsModel, OrganizationsModel

class BalanceOrganizationSerializer(ModelSerializer):
    class Meta:
        model = OrganizationsModel
        fields = ('inn', 'balance')


class WebhookSerialiser(ModelSerializer):
    payer_inn = serializers.CharField(max_length=10)

    class Meta:
        model = PaymentsModel
        fields = ("operation_id", "amount", "payer_inn", "document_number", "document_date")

    def create(self, validated_data):
        inn = validated_data.pop('payer_inn')
        organization = get_object_or_404(OrganizationsModel, inn=inn)
        payment = PaymentsModel.objects.create(payer_inn=organization, **validated_data)
        return payment

from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, mixins, permissions
from django.db import transaction
from django.db import Error

from .models import PaymentsModel, OrganizationsModel
from .serializers import BalanceOrganizationSerializer, WebhookSerialiser
from .services import accrue_sum


class WebhookViewSet(GenericViewSet):
    queryset = PaymentsModel.objects.all()

    @action(methods=['POST'], detail=False)
    def bank(self, request):
        data = WebhookSerialiser(data=request.data)
        try:
            data.is_valid(raise_exception=True)
        except Exception as e:
            if self.queryset.filter(operation_id=request.data.get('operation_id', None)).exists():
                return Response({'status': 'previously processed'}, status=status.HTTP_200_OK)
            raise e
        validated_data = data.validated_data
        with transaction.atomic():
            data.save()
            accrue_sum(org_inn=validated_data.get('payer_inn'), amount=validated_data.get('amount'))
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class OrganizationsViewSet(GenericViewSet):
    queryset = OrganizationsModel.objects.all()

    @action(methods=['GET'], detail=True)
    def balance(self, request, pk):
        data = BalanceOrganizationSerializer(self.get_object())
        return Response(data.data, status=status.HTTP_200_OK)
    
    def get_object(self):
        org = get_object_or_404(OrganizationsModel, inn=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, org)
        return org

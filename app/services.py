from django.db.models import F
from logging import getLogger

from .models import OrganizationsModel


def accrue_sum(org_inn, amount):
    """Начисление суммы на баланс организации"""
    org = OrganizationsModel.objects.filter(inn=org_inn).update(balance=F('balance') + amount)
    if org != 1:
        raise ValueError({'error', f'Ошибка начсиления средств по данному ИНН {org_inn}'})
    logger_balance = getLogger('balance')
    logger_balance.info(msg=f'Зачисление {amount}, по данному ИНН "{org_inn}"')
    return org
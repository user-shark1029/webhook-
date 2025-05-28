from django.db import models
from django.core.validators import MinValueValidator


class OrganizationsModel(models.Model):
    title = models.CharField('Название',
                             max_length=255)
    inn = models.CharField('ИНН',
                           max_length=10,
                           unique=True)
    balance = models.IntegerField('Баланс',
                                  default=0)

    def __str__(self) -> str:
        return self.inn


class PaymentsModel(models.Model):
    operation_id = models.CharField('ID операции',
                                    max_length=100,
                                    unique=True)
    amount = models.IntegerField('Сумма')
    payer_inn = models.ForeignKey(OrganizationsModel,
                                  on_delete=models.CASCADE,
                                  verbose_name='Организация',
                                  related_name='payments')
    document_number = models.CharField('Номер документа',
                                       max_length=60)
    document_date = models.DateTimeField('Дата документа')

    def __str__(self) -> str:
        return self.operation_id
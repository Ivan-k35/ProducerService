from django.db import models


class PurchaseCheck(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True, verbose_name='Идентификатор транзакции')
    timestamp = models.DateTimeField(verbose_name='Дата и время')
    place_id = models.CharField(null=True, blank=True, max_length=255, verbose_name='Идентификатор места')
    place_name = models.CharField(null=True, blank=True, max_length=255, verbose_name='Название места')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма')
    nds_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма НДС')
    tips_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                      verbose_name='Сумма чаевых')
    payment_method = models.CharField(null=True, blank=True, max_length=100, verbose_name='Метод оплаты')

    def __str__(self):
        return f'Покупка {self.transaction_id}'


class Item(models.Model):
    purchase_check = models.ForeignKey(PurchaseCheck, related_name='items', on_delete=models.CASCADE,
                                       verbose_name='Чек покупки')
    product_id = models.CharField(max_length=255, verbose_name='Идентификатор продукта')
    quantity = models.IntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    category = models.CharField(max_length=100, verbose_name='Категория')

    def __str__(self):
        return f'Продукт {self.product_id} в {self.purchase_check}'

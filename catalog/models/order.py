# Description: 
# Author: Kireev Georgiy <metallerok@gmail.com>
# Copyright (C) 2019 by Kireev Georgiy

from django.db import models
from .dish import Dish
from enum import Enum


class OrderStatus(Enum):
    TEMP = 1
    TRANSFERRED_TO_PROCESSING = 2
    PROCESSING = 3
    COMPLETE = 4


class Order(models.Model):
    status = models.IntegerField(choices=[(tag.value, tag.name) for tag in OrderStatus], help_text="Статус заказа")
    price = models.IntegerField(editable=False, null=False, help_text="Сумма заказа", default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    @staticmethod
    def get_current_temp_order(session):
        order_id = session.get('order_id', False)
        if order_id:
            return Order.objects.filter(pk=order_id, status=OrderStatus.TEMP.value).first()

    def recalc_order_price(self):
        self.price = 0
        for dish_in_order in self.order_dish.all():
            self.price += dish_in_order.count * dish_in_order.dish.price
        self.save()

    def __str__(self):
        return "Заказ: %s, Статус: %s" % (self.pk, self.status)

    class Meta:
        verbose_name_plural = "Orders"


class OrderCustomerInfo(models.Model):
    customer_name = models.CharField(max_length=120, help_text="Имя")
    customer_phone = models.CharField(max_length=12, help_text="Телефон")
    customer_email = models.EmailField(null=True, blank=True, help_text="email")
    customer_street = models.CharField(max_length=120, help_text="Улица")
    customer_house_num = models.IntegerField(help_text="Дом")
    customer_housing = models.CharField(max_length=4, null=True, blank=True, help_text="Корпус")
    customer_apartment_num = models.IntegerField(help_text="Квартира")
    order = models.ForeignKey(Order, models.SET_NULL, null=True)

    def __str__(self):
        return "Заказ пользователя: %s" % self.customer_name

    class Meta:
        verbose_name = "Order customer info"
        verbose_name_plural = "Orders customer info"


class OrderDish(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='order_dish')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True)
    count = models.IntegerField(help_text="Кол-во", default=1)

    def save(self, *args, **kwargs):
        dish_in_order = self.order.order_dish.filter(dish=self.dish)
        if dish_in_order:
            dish_in_order.update(count=dish_in_order.first().count+1)
        else:
            super(OrderDish, self).save(*args, **kwargs)

        self.order.recalc_order_price()

    def __str__(self):
        return "Блюдо: %s -> Заказ: %s" % (self.dish.title, self.order.pk)

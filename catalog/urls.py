# Description: catalog urls
# Author: Kireev Georgiy <metallerok@gmail.com>
# Copyright (C) 2019 by Kireev Georgiy

from django.urls import path
from catalog.views import index, category, order

urlpatterns = [
    path('', index.run, name='index'),
    path('<str:slug>', category.CategoryView.as_view(), name='category'),
    path('order/add_dish/<int:id>', order.add_dish, name='order-dish_add'),
    path('order/remove_dish/<int:id>', order.remove_dish, name='order-dish_remove'),
    path('order/clear_dish/<int:id>', order.clear_dish, name='order-dish_clear'),
    path('order/check_order', order.check_order, name='order-check_order'),
    path('order/processed_to_checkout', order.ProcessedToCheckoutView.as_view(), name='order-processed_to_checkout'),
    path('order/confirm', order.confirm, name='order-confirm')
]

# Description: index view
# Author: Kireev Georgiy <metallerok@gmail.com>
# Copyright (C) 2019 by Kireev Georgiy
from django.shortcuts import render
from catalog.models import Dish, Category, Order


def run(request):
    categories = Category.get_categories_with_dishes()
    dishes = Dish.objects.filter(is_draft=False)

    order = Order.get_current_temp_order(request.session)

    if order:
        for dish in dishes:
            dish_in_order = order.order_dish.filter(dish=dish).first()
            if dish_in_order:
                dish.count = dish_in_order.count

    return render(request,
                  'catalog/index.html',
                  context={
                      'categories': categories,
                      'dishes': dishes,
                      'order': order
                  })

# Description: category view
# Author: Kireev Georgiy <metallerok@gmail.com>
# Copyright (C) 2019 by Kireev Georgiy

from django.views import generic
from django.shortcuts import get_object_or_404
from catalog.models import Category, Dish, Order


class CategoryView(generic.ListView):

    template_name = 'catalog/category_view.html'
    context_object_name = 'dishes'
    category = ''

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        order = Order.get_current_temp_order(self.request.session)

        dishes = Dish.objects.filter(category=self.category, is_draft=False)
        if order:
            for dish in dishes:
                dish_in_order = order.order_dish.filter(dish=dish).first()
                if dish_in_order:
                    dish.count = dish_in_order.count
        return dishes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.get_categories_with_dishes()
        order = Order.get_current_temp_order(self.request.session)
        context['current_category'] = self.category
        context['categories'] = categories
        context['order'] = order
        return context

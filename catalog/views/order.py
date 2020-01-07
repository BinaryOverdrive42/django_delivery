# Description: 
# Author: Kireev Georgiy <metallerok@gmail.com>
# Copyright (C) 2019 by Kireev Georgiy
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse_lazy
from catalog.models.order import Order, OrderStatus, OrderDish, Dish
from catalog.forms.order_customer_form import OrderCustomerForm


@require_http_methods(["POST"])
def add_dish(request, id):
    """
    add one dish in order
    :param request:
    :param id:  dish id
    :return: JsonResponse
    """

    # try get order from session, if it doesn't exist create new temp order
    order = Order.get_current_temp_order(request.session)
    if not order:
        order = Order.objects.create(status=OrderStatus.TEMP.value)

    # if dish already in order -> increase dish count
    dish = Dish.objects.get(pk=id)
    OrderDish.objects.create(dish=dish, order=order)
    dish_in_order = order.order_dish.get(dish=dish)
    order.save()
    request.session['order_id'] = order.pk
    dish_list_inline_template = render_to_string('catalog/includes/dish_list_inline.html',
                                                 context={'order': order})
    data = {
        "data": id,
        "events": [
            {
                "event_id": "em_updateDishCount",
                "data": {
                    "dish_id": dish.pk,
                    "count": dish_in_order.count
                }
            },
            {
                "event_id": "em_updateOrderPrice",
                "data": {
                    "price": order.price
                }
            },
            {
                "event_id": "em_html_replace",
                "data": {
                    "element": "#c_dishes-inline",
                    "html": dish_list_inline_template
                }
            },
        ]
    }
    return JsonResponse(data)


@require_http_methods(["POST"])
def remove_dish(request, id):
    """
    remove one dish from order
    :param request:
    :param id: dish id
    :return: JsonResponse
    """

    # try get order from session
    order = Order.get_current_temp_order(request.session)
    dish_count = 0
    dish = Dish.objects.get(pk=id)

    dish_in_order = order.order_dish.filter(dish=dish)
    if dish_in_order and dish_in_order.first().count > 1:
        dish_count = dish_in_order.first().count
        dish_in_order.update(count=dish_count - 1)
        order.recalc_order_price()
    elif dish_in_order and dish_in_order.first().count <= 1:
        dish_in_order.delete()
        order.recalc_order_price()

    dish_list_inline_template = render_to_string('catalog/includes/dish_list_inline.html',
                                                 context={'order': order})
    data = {
        "data": id,
        "events": [
            {
                "event_id": "em_updateDishCount",
                "data": {
                    "dish_id": dish.pk,
                    "count": dish_count
                }
            },
            {
                "event_id": "em_updateOrderPrice",
                "data": {
                    "price": order.price
                }
            },
            {
                "event_id": "em_html_replace",
                "data": {
                    "element": "#c_dishes-inline",
                    "html": dish_list_inline_template
                }
            }
        ]
    }
    return JsonResponse(data)


@require_http_methods(["POST"])
def clear_dish(request, id):
    """
    remove all dish instance from order
    :param request:
    :param id: dish id
    :return: JsonResponse
    """

    # try get order from session
    order = Order.get_current_temp_order(request.session)
    dish = Dish.objects.get(pk=id)

    dish_in_order = order.order_dish.filter(dish=dish)
    if dish_in_order:
        dish_in_order.delete()
        order.recalc_order_price()

    dish_list_inline_template = render_to_string('catalog/includes/dish_list_inline.html',
                                       context={'order': order})
    data = {
        "data": id,
        "events": [
            {
                "event_id": "em_updateDishCount",
                "data": {
                    "dish_id": dish.pk,
                    "count": 0
                }
            },
            {
                "event_id": "em_updateOrderPrice",
                "data": {
                    "price": order.price
                }
            },
            {
                "event_id": "em_html_replace",
                "data": {
                    "element": "#c_dishes-inline",
                    "html": dish_list_inline_template
                }
            }
        ]
    }
    return JsonResponse(data)


@require_http_methods(['POST'])
def check_order(request):
    order = Order.get_current_temp_order(request.session)
    if not order or order.order_dish.all().count() == 0:
        return JsonResponse({
            "events": [
                {
                    "event_id": "em_message",
                    "data": {
                        "type": "alert",
                        "text": "Ваш заказ пуст!"
                    }
                }
            ]
        })
    print(reverse_lazy('order-processed_to_checkout'))
    return JsonResponse({
        "events": [
            {
                "event_id": "em_redirect",
                "data": reverse_lazy('order-processed_to_checkout')
            }
        ]
    })


class ProcessedToCheckoutView(FormView):
    template_name = 'catalog/processed_to_checkout.html'
    form_class = OrderCustomerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.get_current_temp_order(self.request.session)
        context['order'] = order
        context['basket_hide'] = True
        return context


@require_http_methods(['POST'])
def confirm(request):
    form = OrderCustomerForm(request.POST)
    if form.is_valid():
        return JsonResponse({
            "events": [
                {
                    "event_id": "em_message",
                    "data": {
                        "type": "info",
                        "text": "Заказ передан в обработку, ожидайте звонка оператора"
                    }
                }
            ]
        })
    else:
        return JsonResponse({
            "events": [
                {
                    "event_id": "em_form_invalidate",
                    "data": {
                        "prefix": form.prefix,
                        "errors": form.errors.as_json()
                    }

                }
            ]
        })

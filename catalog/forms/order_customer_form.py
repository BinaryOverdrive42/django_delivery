# Description: 
# Author: Kireev Georgiy <metallerok@gmail.com>
# Copyright (C) 2019 by Kireev Georgiy
import re

from django import forms
from catalog.models import OrderCustomerInfo


class OrderCustomerForm(forms.ModelForm):
    prefix = 'customer_info_form'

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('customer_phone')

        r = re.compile(r'((\+7|8)+([0-9]){10})')
        if not r.findall(phone):
            self.add_error('customer_phone', "Неверный формат номера")

    class Meta:
        model = OrderCustomerInfo
        fields = [
            'customer_name',
            'customer_phone',
            'customer_email',
            'customer_street',
            'customer_house_num',
            'customer_housing',
            'customer_apartment_num'
        ]
        labels = {
            "customer_name": "Ваше имя",
            "customer_phone": "Телефон для связи",
            "customer_email": "Email",
            "customer_street": "Улица",
            "customer_house_num": "Дом",
            "customer_housing": "Корпус",
            "customer_apartment_num": "Квартира"
        }

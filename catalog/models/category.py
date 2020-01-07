# Description: category model
# Author: Kireev Georgiy <metallerok@gmail.com>
# Copyright (C) 2019 by Kireev Georgiy

from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=200, help_text="Название категории")
    slug = models.CharField(max_length=200, help_text="slug", unique=True)
    description = models.TextField(max_length=1000, help_text="Описание категории", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    @staticmethod
    def get_categories_with_dishes():
        return Category.objects.annotate(dish_count=models.Count('dish')).filter(is_active=True, dish_count__gt=0)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

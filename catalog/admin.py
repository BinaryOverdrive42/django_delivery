from django.contrib import admin
from .models import Category, Dish, DishImage, OrderDish, OrderCustomerInfo, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')


class DishImageInline(admin.TabularInline):
    model = DishImage
    extra = 0


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_draft']
    inlines = [DishImageInline]


@admin.register(DishImage)
class DishImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'dish', 'is_main_image', 'is_active']


# @admin.register(OrderDish)
# class OrderDishesAdmin(admin.ModelAdmin):
#     pass


class OrderDishesAdminInline(admin.TabularInline):
    model = OrderDish
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDishesAdminInline]


@admin.register(OrderCustomerInfo)
class OrderCustomerInfo(admin.ModelAdmin):
    model = OrderCustomerInfo


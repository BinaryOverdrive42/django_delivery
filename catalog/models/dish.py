# Description: dish model
# Author: Kireev Georgiy <metallerok@gmail.com>
# Copyright (C) 2019 by Kireev Georgiy

import os
from uuid import uuid4
from std import is_valid_uuid
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from PIL import Image
from resizeimage import resizeimage
from django.conf import settings
from .category import Category
from delivery.storage import OverwriteStorage


class Dish(models.Model):
    title = models.CharField(max_length=128, help_text="Название блюда")
    description = models.TextField(max_length=1000, help_text="Описание блюда", null=True, blank=True)
    price = models.IntegerField(help_text="Цена")
    calorific_value = models.IntegerField(help_text="Калорийность", null=True, blank=True)
    proteins = models.FloatField(help_text="Белки", null=True, blank=True)
    fats = models.FloatField(help_text="Жиры", null=True, blank=True)
    carbohydrates = models.FloatField(help_text="Углеводы", null=True, blank=True)
    category = models.ManyToManyField(Category, help_text="Категории")
    is_draft = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Dishes'

    def __str__(self):
        return self.title


class DishImage(models.Model):
    upload_path = "uploads/dish_images/"
    upload_path_thumbs = upload_path + "thumbs/"

    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, related_name='images')
    image = models.ImageField(upload_to=upload_path, unique=True)
    thumbnail = models.ImageField(upload_to=upload_path_thumbs, editable=False, storage=OverwriteStorage())
    is_main_image = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        image_name, image_extension = os.path.splitext(self.image.name)

        # check filename without path
        if not is_valid_uuid(image_name.split('/')[-1]):
            self.image.name = "%s%s" % (uuid4(), image_extension)

        if not self._make_thumbnail():
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(DishImage, self).save(*args, **kwargs)

    def _make_thumbnail(self):
        """
        create thumbnail for uploaded image
        :return: bool
        """

        thumb = Image.open(self.image)
        thumb = resizeimage.resize_cover(thumb, [330, 220])

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name.split('/')[-1] + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        thumb.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

    def __str__(self):
        return "%s" % self.image

    class Meta:
        verbose_name = 'Dish image'
        verbose_name_plural = 'Dish images'

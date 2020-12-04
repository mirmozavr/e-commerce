from PIL import Image

from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class NotebookAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe("<span style='color:red; font-size:13px;'>Minimum image resolution {}x{}, maximum image resolution {}x{}</span>".format(*Product.MIN_RESOLUTION, *Product.MAX_RESOLUTION))

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Image size is bigger than required')
        if img.height < Product.MIN_RESOLUTION[0] or img.width < Product.MIN_RESOLUTION[1]:
            raise ValidationError('Image resolution is smaller than required')
        if img.height > Product.MAX_RESOLUTION[0] or img.width > Product.MAX_RESOLUTION[1]:
            raise ValidationError('Image resolution is bigger than required')
        return image


class NotebookAdmin(admin.ModelAdmin):
    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug="notebooks"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug="smartphones"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)

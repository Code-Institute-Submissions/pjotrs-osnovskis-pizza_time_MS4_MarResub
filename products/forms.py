from django import forms
from .models import Category, Product, Topping
from django.forms.widgets import CheckboxSelectMultiple
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('name', 'likes',)

    image_path = forms.ImageField(label='Product Image', required=False,
                                  widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        toppings = Topping.objects.all()
        display_names = [(c.id, c.get_display_name()) for c in categories]

        # Giving Toppings a checkboxes instead of list, and pressing a
        # CTRL+"click". Solution was found here:
        # https://chase-seibert.github.io/blog/2010/05/20/
        # django-manytomanyfield-on-modelform-as-checkbox-widget.html

        self.fields['toppings'].widget = CheckboxSelectMultiple()
        self.fields['toppings'].queryset = toppings

        self.fields['category'].choices = display_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'product-admin-inputs'

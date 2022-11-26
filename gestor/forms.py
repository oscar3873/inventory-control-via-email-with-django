import html
from django import forms
from gestor.models import Producto
from django.forms.widgets import NumberInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('marca', 'producto', 'tipo','fechaIngreso', 'fechaVnto','stockIng', 'stockDisp')
        widgets = {'fechaIngreso': NumberInput(attrs={'type': 'date'}),'fechaVnto': NumberInput(attrs={'type': 'date'}),}

import datetime
import html
from django import forms
from django.forms import DateInput
from gestor.models import EventMember, Evento, Producto
from django.forms.widgets import NumberInput
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout

class ProductoForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['stockDisp'].disabled = True

    class Meta:
        model = Producto
        fields = ('marca', 'producto', 'tipo','fechaIngreso','fechaEnvasado', 'fechaVnto','stockIng','codBulto')
        widgets = {
            'fechaIngreso': NumberInput(attrs={'type': 'date'}),
            'fechaVnto': NumberInput(attrs={'type': 'date'}),
            'fechaEnvasado': NumberInput(attrs={'type': 'date'}),
            }

    def clean(self):
        """ super(ProductoForm, self).clean() """
        marca = self.cleaned_data.get('marca')
        producto = self.cleaned_data.get('producto')
        tipo = self.cleaned_data.get('tipo')
        fechaIngreso = self.cleaned_data.get('fechaIngreso')
        fechaVnto = self.cleaned_data.get('fechaVnto')
        fechaEnvasado = self.cleaned_data.get('fechaEnvasado')
        stockIng = self.cleaned_data.get('stockIng')
        # stockDisp = self.cleaned_data.get('stockIng')
        codigoBulto = self.cleaned_data.get('codBulto')
        
        if type(marca)==type(None):
            self._errors['marca'] = self.error_class(['Campo obligatorio.'])

        if type(producto) == type(None):
            self._errors['producto'] = self.error_class(['Campo obligatorio.'])

        if type(tipo) == type(None):
            self._errors['tipo'] = self.error_class(['Campo obligatorio.'])

        if fechaIngreso==None:
            self._errors['fechaIngreso'] = self.error_class(['Campo obligatorio.'])

        if fechaEnvasado==None:
            self._errors['fechaEnvasado'] = self.error_class(['Campo obligatorio.'])

        if fechaVnto==None:
            self._errors['fechaVnto'] = self.error_class(['Campo obligatorio.'])

        if fechaIngreso!=None and fechaVnto!=None:
            if fechaVnto<fechaIngreso:
                self._errors['fechaVnto'] = self.error_class(['La fecha de vencimiento debe ser posterior a la del ingreso.'])

        if fechaIngreso!=None and fechaEnvasado!=None:
            if fechaIngreso<fechaEnvasado:
                self._errors['fechaEnvasado'] = self.error_class(['La fecha de envasado debe ser anterior a la del ingreso.'])

        if fechaVnto<=datetime.date.today():
            self._errors['fechaVnto'] = self.error_class(['No es posible cargar producto vencido.'])
    
        if type(stockIng) == type(None):
            self._errors['stockIng'] = self.error_class(['Campo obligatorio.'])
        elif stockIng <= 0:
            self._errors['stockIng'] = self.error_class(['El numero ingresado debe ser mayor a cero.'])

        # if type(stockDisp) == type(None):
        #     self._errors['stockDisp'] = self.error_class(['Campo obligatorio.'])
        # elif stockDisp <= 0:
        #     self._errors['stockDisp'] = self.error_class(['El numero ingresado debe ser mayor a cero.'])

        # if type(stockIng) != type(None) and type(stockDisp) != type(None):
        #     if stockIng < stockDisp:
        #         self._errors['stockDisp'] = self.error_class(['El stock disponible debe ser menor o igual al stock de ingreso.'])

        if type(codigoBulto) == type(None):
            self._errors['codigoBulto'] = self.error_class(['Campo obligatorio.'])
        elif codigoBulto == '':
            self._errors['codigoBulto'] = self.error_class(['El numero ingresado debe ser mayor a cero.'])
        
        return self.cleaned_data


class EventForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ["titulo", "descripcion", "tiempo_inicio", "tiempo_fin"]
        # datetime-local is a HTML5 input type
        widgets = {
            "titulo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event title"}
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                }
            ),
            "tiempo_inicio": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "tiempo_fin": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["tiempo_inicio"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["tiempo_fin"].input_formats = ("%Y-%m-%dT%H:%M",)


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["usuario"]
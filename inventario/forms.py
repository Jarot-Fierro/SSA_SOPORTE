from django import forms

from .models import InventarioMantencion, InventarioInformatica


class FormInventarioMantencion(forms.ModelForm):
    class Meta:
        model = InventarioMantencion
        fields = [
            'producto',
            'descripcion',
            'unidad',
            'tipo_material',
            'tipo_compra',
            'codigo',
            'stock_actual',
            'stock_minimo',
            'stock_maximo',
            'ubicacion',
            'lote',
            'fecha_vencimiento',
            'categoria'
        ]

        widgets = {
            'producto': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'producto_inventario_mant'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'id': 'descripcion_inventario_mant'
            }),
            'unidad': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'tipo_material': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'tipo_compra': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'stock_actual': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'stock_maximo': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'lote': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    # ✅ Validación nombre único (case insensitive)
    def clean_producto(self):
        producto = self.cleaned_data['producto'].strip()

        qs = InventarioMantencion.objects.filter(producto__iexact=producto)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Ya existe un producto con ese nombre")

        return producto

    # ✅ Validación código único
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')

        if codigo:
            qs = InventarioMantencion.objects.filter(codigo=codigo)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("Ya existe un producto con ese código")

        return codigo

    # ✅ Validación lógica de stock
    def clean(self):
        cleaned_data = super().clean()

        stock_min = cleaned_data.get('stock_minimo')
        stock_max = cleaned_data.get('stock_maximo')

        if stock_max is not None and stock_min is not None:
            if stock_max < stock_min:
                self.add_error('stock_maximo', 'El stock máximo no puede ser menor al mínimo')

        return cleaned_data


class FormInventarioTIC(forms.ModelForm):
    class Meta:
        model = InventarioInformatica
        fields = [
            'producto',
            'descripcion',
            'unidad',
            'tipo_material',
            'tipo_compra',
            'codigo',
            'stock_actual',
            'stock_minimo',
            'stock_maximo',
            'ubicacion',
            'lote',
            'fecha_vencimiento',
            'categoria'
        ]

        widgets = {
            'producto': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'producto_inventario_tic'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'id': 'descripcion_inventario_tic'
            }),
            'unidad': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'tipo_material': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'tipo_compra': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'stock_actual': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'stock_maximo': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'lote': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    # ✅ Validación nombre único (case insensitive)
    def clean_producto(self):
        producto = self.cleaned_data['producto'].strip()

        qs = InventarioInformatica.objects.filter(producto__iexact=producto)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Ya existe un producto con ese nombre")

        return producto

    # ✅ Validación código único
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')

        if codigo:
            qs = InventarioInformatica.objects.filter(codigo=codigo)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("Ya existe un producto con ese código")

        return codigo

    # ✅ Validación lógica de stock
    def clean(self):
        cleaned_data = super().clean()

        stock_min = cleaned_data.get('stock_minimo')
        stock_max = cleaned_data.get('stock_maximo')

        if stock_max is not None and stock_min is not None:
            if stock_max < stock_min:
                self.add_error('stock_maximo', 'El stock máximo no puede ser menor al mínimo')

        return cleaned_data

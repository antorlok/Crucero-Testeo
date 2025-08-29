from django import forms
from .models import Proveedores, Material

class ProveedorForm(forms.ModelForm):
    materiales = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Materiales'
    )

    class Meta:
        model = Proveedores
        fields = '__all__'

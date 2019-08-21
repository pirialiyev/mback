from django import forms
from products.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class AddProducts(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Elave et'))
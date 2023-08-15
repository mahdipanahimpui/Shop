from django import forms
from django.core.exceptions import ValidationError



class CartAddForm(forms.Form):
    quantity = forms.IntegerField()


    def clean_quantity(self):
                # use clean_pass2 not clean pass1 because pass2 is not define in validation
        quantity = self.cleaned_data['quantity']
        print('quantity')


        if not (1 <= quantity <= 10):
            print('in if')
            raise ValidationError('limit: 1 to 10')
        return quantity
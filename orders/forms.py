from django import forms



class CartAddForm(forms.Form):
    quantitiy = forms.IntegerField(min_value=1, max_value=10)


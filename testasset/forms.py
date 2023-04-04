from django.forms import ModelForm
from .models import  Staff, Asset
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# class OrderForm(ModelForm):
#     class Meta:
#         model = Order
#         fields = '__all__'

class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'
        widgets = {
            'warranty_start': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd'}),
            'warranty_end': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd'}),

        }

    # def clean_asset_no(self):
    #     id = self.data['id'] if self.data['id'] != '' else 0
    #     asset_no = self.cleaned_data['asset_no']
    #     try:
    #         if id > 0:
    #             asset_no = Asset.exclude(id=id).get(asset_no = asset_no)
    #         else:
    #             asset_no = Asset.get(asset_no = asset_no)
    #     except:
    #         return asset_no
    #     return forms.ValidationError(f"{asset_no} already exists.")
        

        
class DateInput(forms.DateInput):
    input_type = 'date'




from django.forms import ModelForm, DateInput
from .models import  *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'
        widgets = {
            'joining_date': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd'}),
        }

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


class EventForm(forms.ModelForm):
  class Meta:
    model = Event
    fields = '__all__'
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'warranty_start': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd'}),
      'warranty_end': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd'}),
    }
    

#   def __init__(self, *args, **kwargs):
#     super(EventForm, self).__init__(*args, **kwargs)
#     # input_formats to parse HTML5 datetime-local input to datetime field
#     self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
#     self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)



class AddCategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'

class AddDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
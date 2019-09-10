from django import forms
from django.forms import ModelForm
from .models import *
from django.forms import formset_factory


class RegulationForm(forms.Form):
    regulations=Regulations.objects.values_list('regulation','regulation')
    choices = (
        regulations
    )
    Regulations=forms.CharField(label='Select Regulations', widget=forms.RadioSelect(choices=choices))
    #Regulations = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=choices)
    #risk = forms.CharField(label='Select Level of Risk', widget=forms.RadioSelect(choices=OPTIONS))
    '''
    comment = forms.CharField(
        label='Regulations comment',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Comment',
            'required':'This Field is Required'
        })
    ) '''

class BusinessForm(forms.Form):
    objects = BusinessActivity.objects.values_list('businessdefinition','businessdefinition')
    options = (
            objects
        )
    BusinessActivitites = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=options)

class CustomBusinessForm(forms.Form):
    class Meta:
        model = BusinessActivity

    businessdefinition_q = forms.CharField(
        label='Business Definition Question',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Business Definition Question'
        })
    )
    businessdefinition_a = forms.CharField(
        label='Business Definition Answer',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Business Definition Answer'
        })
    )
    jurisdiction = forms.CharField(
        label='Jurisdiction',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Jurisdiction'
        })
    )
    
CustomBusinessFormSet = formset_factory(CustomBusinessForm)


# class ProcessForm(ModelForm):
#     class Meta:
#         model = BAReg
#         fields = []
     

#     objects = Process.objects.values_list('process','process')
    
#     OPTIONS = (
#         objects
#     )


#     process = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
#                                           choices=OPTIONS)





class ProcessForm(forms.Form):
    title = forms.CharField(
        label='Process Title',
        widget=forms.TextInput(attrs={'required': 'true',
            'class': 'form-control',
            'placeholder': 'Enter Process Title here',
            'required':'This Field is Required'
        })
    )
    description = forms.CharField(
        label='Process Description',
        widget=forms.TextInput(attrs={'required': 'true',
            'class': 'form-control',
            'placeholder': 'Enter Process Description',
            'required':'This Field is Required'
        })
    )
    
ProcessFormSet = formset_factory(ProcessForm)


     
# class ControlsForm(ModelForm):
#     class Meta:
#         model= ProcessReg
#         fields = []
#     objects = Controls.objects.values_list('control','control')

#     OPTIONS = (
#         objects
#     )

#     controls = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
#                                           choices=OPTIONS)


class ControlForm(forms.Form):
    control = forms.CharField(
        label='Control Title',
        widget=forms.TextInput(attrs={'required': 'true',
            'class': 'form-control',
            'placeholder': 'Enter Control Area',
            'required':'This Field is Required'
        })
    )
    description = forms.CharField(
        label='Control Description',
        widget=forms.TextInput(attrs={'required': 'true',
            'class': 'form-control',
            'placeholder': 'Enter Control Description',
            'required':'This Field is Required'
        })
    )
    content = forms.CharField(
        label='Control Content',
        widget=forms.TextInput(attrs={'required': 'true',
            'class': 'form-control',
            'placeholder': 'Enter Control Objective',
            'required':'This Field is Required'
        })
    )
ControlFormSet = formset_factory(ControlForm)
     
class RiskForm(ModelForm):
    class Meta:
        model= ControlReg
        fields = []
    OPTIONS = [
          ('Low', 'Low'),
          ('Medium', 'Medium'),
          ('High','High')
    ]

    risk = forms.CharField(label='Select Level of Risk', widget=forms.RadioSelect(choices=OPTIONS))
    comment = forms.CharField(
        label='Risk comment',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Comment',
            'required':'This Field is Required'
        })
    )
RiskFormSet = formset_factory(RiskForm)

class EditbaForm(ModelForm):  
    class Meta:
        regulations=Regulations.objects.values_list('regulation','regulation')
        reg = (
        regulations
        )
        objects = BusinessActivity.objects.values_list('businessdefinition_a','businessdefinition_a')
    
        options = (
        objects
    )
        model = BAReg
        fields = ['regulation','businessdefinition_a']
        widgets = {
           'regulation': forms.Select(choices = reg),
           'businessdefinition_a': forms.Select(choices = options)
       }
    
class EditprocessForm(ModelForm):
     class Meta:
          objects = Process.objects.values_list('process','process')
          options = (
          objects
            )
          model = ProcessReg
          fields = ['process']
          widgets = {
              'process' : forms.Select(choices=options)
          }

class EditcontrolForm(ModelForm):
     class Meta:
          objects = Controls.objects.values_list('content','content')
          options=(
              objects
          )
          model = ControlReg
          fields = ['controlarea']
          widgets = {
              'controlarea' : forms.Select(choices=options)
          }

class EditriskForm(ModelForm):
     class Meta:
          objects = Risk.objects.values_list('risk','risk')
          options=(
              objects
          )
          model = RiskReg
          fields = ['risk']
          widgets = {
              'risk' : forms.Select(choices=options)
          }
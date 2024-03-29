from django import forms
from devices.models import Device


class DeviceForm(forms.ModelForm):
    # required_css_class = 'required'

    class Meta:
        model = Device
        fields = [
            'name',
            'device_type',
            'device_id',
            'lane_1',
            'enable_1',
            'lane_2',
            'enable_2',
            'lane_3',
            'enable_3',
            'lane_4',
            'enable_4',
            'lane_5',
            'enable_5',
            'lane_6',
            'enable_6',
            'lane_7',
            'enable_7',
            'lane_8',
            'enable_8',
            'description',
            'state',
            'city',
            'lat',
            'lng',
        ]

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'device_image': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'id' : 'customFile',
                    'required': False,
                }
            ),
            'lane_1': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'enable_1': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'type': 'checkbox',
                    'id': 'enable_1',
                    'onclick': 'checkbox_click(this)',
                }
            ),

            'lane_2': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'enable_2': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'type': 'checkbox',
                    'id': 'enable_2',
                    'onclick': 'checkbox_click(this)',
                }
            ),

            'lane_3': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'enable_3': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'type': 'checkbox',
                    'id': 'enable_3',
                    'onclick': 'checkbox_click(this)',
                }
            ),

            'lane_4': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'enable_4': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'type': 'checkbox',
                    'id': 'enable_4',
                    'onclick': 'checkbox_click(this)',
                }
            ),
            'lane_5': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'enable_5': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'type': 'checkbox',
                    'id': 'enable_5',
                    'onclick': 'checkbox_click(this)',
                }
            ),
            'lane_6': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'enable_6': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'type': 'checkbox',
                    'id': 'enable_6',
                    'onclick': 'checkbox_click(this)',
                }
            ),
            'lane_7': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'enable_7': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'type': 'checkbox',
                    'id': 'enable_7',
                    'onclick': 'checkbox_click(this)',
                }
            ),
            'lane_8': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'enable_8': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'type': 'checkbox',
                    'id': 'enable_8',
                    'onclick': 'checkbox_click(this)',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                }
            ),
            'state': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'city': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'lat': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'lng': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        

            'remote_address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': False,
                }
            ),

            'enable': forms.CheckboxInput(
                attrs={
                    'class': 'form-control'
                }
            ),

        }

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control'
            if i not in ['enable']:
                self.fields[i].widget.attrs['class'] = 'form-control'

class DeviceField(forms.ModelForm):
    device_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))  
    class Meta:
        model = Device
        fields = ['device_images']



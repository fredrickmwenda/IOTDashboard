from django import forms
# from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm

from devices.models import Device
from .models import UserDevices, UserProfile
import logging

User = get_user_model()

logger = logging.getLogger(__name__)

class LoggingMixin(object):
    def add_error(self, field, error):
        if field:
            logger.info('Form error on field %s: %s', field, error)
        else:
            logger.info('Form error: %s', error)
        super().add_error(field, error)

class UserAdminCreationForm(forms.ModelForm, LoggingMixin):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ['email', 'full_name', ]

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email','full_name', 'password', 'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]










class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))

    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Fullname",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control"
            }
        ))


    class Meta:
        model = User
        fields = ('email','full_name',  'password1', 'password2',)




    def clean_password(self):
        '''
        Verify both passwords match.
        '''
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

 
class CreateUsers(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    
    phone_number = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Phone Number",
                "class": "form-control"
            }
        ))

    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Fullname",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control"
            }
        ))
#     


    class Meta:
        model = User
        fields = ('email','full_name',  'phone_number', 'password1', 'password2', 'admin', 'staff', 'normal_user', 'advanced_user',)




    def clean_password(self):
        '''
        Verify both passwords match.
        '''
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(CreateUsers, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user












class CreateUserDevice(forms.ModelForm):
    
    class Meta:
        model = UserDevices
        fields = [
            # 'user_detail',
            'device_name',
            'device_type',
            'device_id',
            'lane1',
            'lane2',
            'lane3',
            'lane4',
            'lane1_status',
            'lane2_status',
            'lane3_status',
            'lane4_status',
            'device_status',
            'city',
            'state',
            'lat',
            'lng',               
        ]
        

        widgets = {
            'user_details': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'device_name': forms.Select(
                
                attrs={
                    "class": "form-control"
                }
            ),

            'device_type': forms.TextInput(
                
                attrs={
                    "class": "form-control"
                }
            ),

            'device_id': forms.TextInput(              
                attrs={
                    "class": "form-control"
                }
            ),

            'lane1': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'lane2': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'lane3': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'lane4': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'lane1_status': forms.RadioSelect(
                 attrs={
                    'class': 'form-control',
                    'id': 'lane1_status'
                }
            ),

            'lane2_status': forms.RadioSelect(
                 attrs={
                    'class': 'form-control',
                    'id': 'lane2_status'
                }
            ),

            'lane3_status': forms.RadioSelect(
                 attrs={
                    'class': 'form-control',
                    'id': 'lane3_status'
                }
            ),

            'lane4_status': forms.RadioSelect(
                 attrs={
                    'class': 'form-control',
                    'id': 'lane4_status'
                
                }
            ),

            'device_image': forms.ClearableFileInput(            
                attrs={
                    "class": "form-control",
                    "multiple": True,
                    "required": False,
                }
            ),

            'device_status': forms.TextInput(
                
                attrs={
                    "class": "form-control"
                }
            ),

            'city': forms.TextInput(
                
                attrs={
                    "class": "form-control"
                }
            ),

            'state': forms.TextInput(
               attrs={
                    "class": "form-control"
                }

            ),
            'lat': forms.NumberInput(
               attrs={
                    "class": "form-control"
                }
            ),

            'lng': forms.NumberInput(
               attrs={
                    "class": "form-control"
                }
            ),

            'lane_1': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'lane_2' :  forms.TextInput(
                attrs={                       
                    "class": "form-control"
                }
            ),

            'lane_3' :  forms.TextInput(
                attrs={                       
                    "class": "form-control"
                }
            ),

            'lane_4' :  forms.PasswordInput(
                attrs={                   
                    "class": "form-control"
                }
            ),

        
        }


class UserDeviceImage(forms.ModelForm):
    device_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))  
    class Meta:
        model = UserDevices
        fields = ['device_images']



    
class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'full_name',
            'user_name',
            'address',
            'country',
            'city',
            'state',
            'zip',
            'about',
            'photo',
            
        ]

        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'user_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'address': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'country': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

           'city': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'state': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'zip': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),



            'about': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),

                        # 'photo': forms.FileInput(
            #     attrs={
            #         'class': 'form-control',
            #         'id' : 'customFile',
            #         'required': False,
            #     }
            # ),



            


        }



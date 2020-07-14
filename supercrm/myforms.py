import re


from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError

from supercrm import models



#自定义电话号码验证
def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')  # 自定义验证规则的时候，如果不符合你的规则，需要自己发起错误


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        min_length=6,
        label='用户名',
        widget=forms.widgets.TextInput(attrs={'class': 'username',
                                              'autocomplete': 'off',
                                              'placeholder': '输入用户名', }),
        error_messages={
            'required': '用户名不能为空',
            'min_length': '用户名不能小于6位',
            'max_length': '用户名不能大于16位',
        }
    )
    password = forms.CharField(
        max_length=32,
        min_length=6,
        label='密码',
        widget=forms.widgets.PasswordInput(attrs={'class': 'password',
                                                  'placeholder': '输入密码',
                                                  'oncontextmenu': 'return false',
                                                  'onpaste': 'return false'
                                                  }),
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码不能小于6位',
            'max_length': '密码不能大于32位',
        }
    )
    r_password = forms.CharField(
        max_length=32,
        min_length=6,
        label='密码',
        widget=forms.widgets.PasswordInput(attrs={'class': 'confirm_password',
                                                  'placeholder': '再次输入密码',
                                                  'oncontextmenu': 'return false',
                                                  'onpaste': 'return false'
                                                  }),
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码不能小于6位',
            'max_length': '密码不能大于32位',
        }
    )

    def clean(self):
        values = self.cleaned_data
        password = values.get('password')
        r_password = values.get('r_password')
        if password == r_password:
            return values
        else:
            self.add_error('r_password', '密码不一致')

    email = forms.EmailField(
        label='邮箱',
        # validators=[]
        error_messages={
            'invalid': '邮箱格式错误',
            'required': '邮箱不能为空',
        },
        widget=forms.widgets.PasswordInput(attrs={'class': 'email',
                                                  'placeholder': '输入邮箱',
                                                  'oncontextmenu': 'return false',
                                                  'type': 'email',
                                                  }),
    )
    telephone = forms.CharField(
        label='手机号不能为空',
        validators=[mobile_validate, ],
        error_messages={'required': '邮箱不能为空', },
        widget=forms.widgets.PasswordInput(attrs={'class': 'phone_number',
                                                  'placeholder': '输入手机号',
                                                  'autocomplete': 'off',
                                                  'id': 'number',
                                                  }),
    )


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customers
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({'class': 'form-control'})


class ConsultRecordForm(forms.ModelForm):
    class Meta:
        model=models.ConsultRecord
        fields= '__all__'
        exclude = ['delete_status']



    def __init__(self, request,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'customer':
                field.queryset=models.Customers.objects.filter(consultant=request.user_obj)
            elif field_name == 'consultant':
                field.queryset=models.UserInfo.objects.filter(pk=request.user_obj.pk)

class EnrollForm(forms.ModelForm):

    class Meta:
        model=models.Enrollment
        fields= '__all__'
        exclude = ['delete_status']

    def __init__(self, request,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'customer':
                field.queryset=models.Customers.objects.filter(consultant=request.user_obj)
            elif field_name == 'consultant':
                field.queryset=models.UserInfo.objects.filter(pk=request.user_obj.pk)


class ScoreForm(forms.ModelForm):

    class Meta:
        model=models.Score
        fields= '__all__'

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'customer':
                field.queryset = models.Customers.objects.filter(consultant=request.user_obj)
            elif field_name == 'consultant':
                field.queryset = models.UserInfo.objects.filter(pk=request.user_obj.pk)


class MoreScoreModelForm(forms.ModelForm):
    class Meta:
        model=models.Score
        fields='__all__'

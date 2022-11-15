from django import forms
from staff_app import models
from staff_app.utils.bootstrap import BootStrapModelForm
from django.core.validators import RegexValidator


class StaffModelFrom(BootStrapModelForm):  # 定义一个类StaffModelFrom
    name = forms.CharField(min_length=2)  # 新增校验，名字最小等于2个字

    class Meta:
        model = models.StaffInfo
        fields = ["name", "password", "age", "salary",
                  "entry_time", "gender", "staff_department"]  # field字段


class MobileModelForm(BootStrapModelForm):
    """靓号管理"""
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}', "手机号格式错误"), ])

    class Meta:
        model = models.MobileNum
        fields = ["mobile", "price", "level", "status"]
        # fields = "__all__" 获取所有models.py中的所有字段
        # exclude = ['level'] 获取models.py中除了level的其他字段


class GoodModelForm(forms.ModelForm):
    class Meta:
        model = models.GoodInfo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

import time  # 先导入内置模块，规律是短的在上面

from django import forms  # 中间导入第三方已安装的模块
from django.shortcuts import render, HttpResponse, redirect

from staff_app import models  # 最后导入我们自定义的模块
from staff_app.utils.pagination import Pagination
from staff_app.utils.form import StaffModelFrom, MobileModelForm

from django import forms
from django.core.exceptions import ValidationError
from staff_app.utils.bootstrap import BootStrapModelForm
from staff_app.utils.encrypt import md5


def admin_list(request):
    """管理员列表"""

    # 检查用户是否已经登录，登录则可以访问，未登录则跳转会登录页码
    # 用户发来请求，获取用户浏览器cookie随机字符串，和网站session中做对比
    info = request.session.get("info")
    if not info:
        return redirect("/login/")

    # 构造搜索
    data_dict = {}
    search_data = request.GET.get('num', "")
    if search_data:
        data_dict["username__contains"] = search_data

    # 根据搜索条件取数据库获取
    queryset = models.Admin.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request, queryset, page_size=4)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
        "search_data": search_data
    }
    return render(request, "admin_list.html", context)


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    # 钩子方法
    def clean_confirm_password(self):
        print(self.cleaned_data)
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")

        # 返回什么，此字段以后保存到数据库就是什么
        return confirm


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        # 去数据库校验当前密码与新输入的密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与之前的相同")

    # 钩子方法
    def clean_confirm_password(self):
        print(self.cleaned_data)
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")

        # 返回什么，此字段以后保存到数据库就是什么
        return confirm


def admin_reset(request, nid):
    """重置密码"""
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, "error.html", {"msg": "数据不存在"})

    title = "重置密码"

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "change.html", {"form": form, "title": title})
    else:
        form = AdminResetModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect("/admin_list/")
        else:
            return render(request, "change.html", {"form": form, "title": title})
            # return HttpResponse("出现错误")


def admin_add(request):
    """添加管理员"""
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change.html", {"form": form, "title": title})
    else:
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/admin_list/")
        else:
            return render(request, "change.html", {"form": form, "title": title})


def admin_edit(request, nid):
    """编辑管理员"""
    # 如果能搜到，则是获取到的是一个对象，搜不到则是None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, "error.html", {"msg": "数据不存在"})

    title = "编辑管理员"
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)  # 显示默认值，instance=rowobject
        return render(request, "change.html", {"form": form, "title": title})
    else:
        form = AdminEditModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect("/admin_list/")
        else:
            return render(request, "change.html", {"form": form, "title": title})


def admin_delete(request, nid):
    """删除管理员"""
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin_list/")

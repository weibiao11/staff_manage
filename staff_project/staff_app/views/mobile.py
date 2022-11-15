from django.shortcuts import render, HttpResponse, redirect
from staff_app import models
from staff_app.utils.pagination import Pagination
from staff_app.utils.form import StaffModelFrom, MobileModelForm
from django import forms


def mobile_list(request):
    """ 靓号列表 """

    """搜索"""
    data_dict = {}  # data_dict等于一个空字典
    search_data = request.GET.get('num', "")
    if search_data:
        # data_dict是一个字典
        # 这是在往字典里面添加数据，key="mobile__contains"，value=search_data
        data_dict["mobile__contains"] = search_data
    # res = models.MobileNum.objects.filter(**data_dict)
    # print(res)

    """分页"""
    queryset = models.MobileNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset, page_size=4)  # 实例化我们自定义的类

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成的页码
    }
    return render(request, 'mobile_list.html', context)


def mobile_add(request):
    """"添加靓号"""
    if request.method == "GET":
        form = MobileModelForm()  # 实例化类的对象
        return render(request, "mobile_add.html", {"form": form})

    form = MobileModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect("/mobile_list/")
    return render(request, 'mobile_add.html', {"form": form})


def mobile_edit(request, nid):
    """编辑靓号"""
    row_object = models.MobileNum.objects.filter(id=nid).first()  # 这行代码勿忘，否则就成新增用户为不是编辑用户了
    if request.method == "GET":
        # 根据ID获取数据库中数据
        form = MobileModelForm(instance=row_object)  # 使用 instance ，ModelForm就可以默认将数据显示出来
        return render(request, 'mobile_edit.html', {"form": form})

    form = MobileModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/mobile_list/')
    # 如果数据不合格，则返回"user_edit.html"
    return render(request, 'mobile_edit.html', {"form": form})


def mobile_delete(request, nid):
    """删除靓号"""
    models.MobileNum.objects.filter(id=nid).delete()
    return redirect("/mobile_list/")

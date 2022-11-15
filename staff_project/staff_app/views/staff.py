from django.shortcuts import render, HttpResponse, redirect
from staff_app import models
from staff_app.utils.pagination import Pagination
from staff_app.utils.form import StaffModelFrom, MobileModelForm
from django import forms


def staff_add(request):
    """添加员工"""
    if request.method == "GET":
        dict0 = {
            'gender_choices': models.StaffInfo.gender_choices,
            'department_list': models.Department.objects.all()  # objects是取的一个对象，包括id和title
        }
        return render(request, "staff_add.html", dict0)
    # 获取用户通过表单提交的数据
    name = request.POST.get("name")
    password = request.POST.get("password")
    age = request.POST.get("age")
    salary = request.POST.get("salary")
    entry_time = request.POST.get("entry_time")
    gender = request.POST.get("gender")
    staff_department_id = request.POST.get("staff_department_id")
    # 添加到数据库中
    models.StaffInfo.objects.create(name=name, password=password, age=age, salary=salary, entry_time=entry_time,
                                    gender=gender, staff_department_id=staff_department_id)
    return redirect("/staff_list/")


def staff_list(request):
    """员工列表"""
    queryset = models.StaffInfo.objects.all()

    page_object = Pagination(request, queryset, page_size=4)

    context = {
        "data_list": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, "staff_list.html", context)


def modelform_staff_add(request):
    """添加员工(ModelForm版本)"""
    if request.method == "GET":
        form = StaffModelFrom()  # 实例化类的对象
        return render(request, "modelform_staff_add.html", {"form": form})  # 将form传入html

    # 用post方式提交数据，数据校验
    form = StaffModelFrom(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/staff_list/")
    # 校验失败
    return render(request, "modelform_staff_add.html", {"form": form})


def staff_edit(request, nid):
    """编辑员工"""
    if request.method == "GET":
        # 以下两行是再编辑页面中展示默认值
        row_object = models.StaffInfo.objects.filter(id=nid).first()
        form = StaffModelFrom(instance=row_object)

        return render(request, "staff_edit.html", {"form": form})

    row_object = models.StaffInfo.objects.filter(id=nid).first()  # 获取到id=nid那一行
    form = StaffModelFrom(data=request.POST, instance=row_object)
    if form.is_valid():
        # form.save()默认保存输入的所有值
        # 想要再田间一个输入以外的值，#form.instance.字段名 = 值
        form.save()
        return redirect("/staff_list/")
    return render(request, 'staff_edit.html', {"form": form})


def staff_delete(request, nid):
    """删除员工"""
    models.StaffInfo.objects.filter(id=nid).delete()
    return redirect("/staff_list/")

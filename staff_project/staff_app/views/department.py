from django.shortcuts import render, HttpResponse, redirect
from staff_app import models
from staff_app.utils.pagination import Pagination
from staff_app.utils.form import StaffModelFrom, MobileModelForm
from django import forms


def department_list(request):
    """部门列表"""
    # queryset是[对象(一行数据)，对象，对象]
    # queryset = models.Department.objects.all()
    queryset = models.Department.objects.all()

    page_object = Pagination(request, queryset, page_size=4)

    context = {
        "data_list": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, "department_list.html", context)


def department_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request, 'department_add.html')
    title = request.POST.get("title")
    # 保存到数据库
    models.Department.objects.create(title=title)
    # 重定向回部门列表
    return redirect("/department_list/")


def department_delete(request):
    """删除部门"""
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect("/department_list/")


def department_edit(request, nid):
    """编辑部门(修改部门)"""
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, "department_edit.html", {"row_object": row_object})
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)

    return redirect("/department_list/")

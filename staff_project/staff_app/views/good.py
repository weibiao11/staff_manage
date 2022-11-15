from django.shortcuts import render, HttpResponse, redirect
from staff_app import models
from staff_app.utils.pagination import Pagination
from staff_app.utils.form import StaffModelFrom, MobileModelForm, GoodModelForm
from django import forms


def good_list(request):
    """商品列表"""
    queryset = models.GoodInfo.objects.all()
    page_object = Pagination(request, queryset, page_size=2)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成的页码
    }
    return render(request, "good_list.html", context)


def good_add(request):
    """新增商品"""
    if request.method == "GET":
        form = GoodModelForm()
        return render(request, "good_add.html", {"form": form})

    form = GoodModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect("/good_list/")
    return render(request, 'good_add.html', {"form": form})


def good_edit(request, nid):
    """编辑商品"""
    row_object = models.GoodInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = GoodModelForm(instance=row_object)
        return render(request, "good_edit.html", {"form": form})
    else:
        form = GoodModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect("/good_list/")
        else:
            return render(request, "good_edit.html", {"form": form})


def good_delete(request, nid):
    """删除商品"""
    models.GoodInfo.objects.filter(id=nid).delete()
    return redirect("/good_list/")

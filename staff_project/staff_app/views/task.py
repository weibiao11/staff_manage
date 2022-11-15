import json
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

from django import forms
from staff_app import models
from staff_app.utils.bootstrap import BootStrapModelForm


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            # "detail":forms.TextInput
            "detail": forms.Textarea
        }


def task_list(request):
    """任务管理列表"""

    form = TaskModelForm()  # 实例化我们自定义的类
    return render(request, "task_list.html", {"form": form})


@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {"status": True, "data": [11, 22, 33, 44]}
    return HttpResponse(json.dumps(data_dict))


@csrf_exempt
def task_add(request):
    print(request.POST)

    # 对用户发过来的数据进行校验（用modelform进行校验）
    form = TaskModelForm(data=request.POST)
    if form.is_valid():  # 如果校验成果执行form.save()
        form.save()  # 将用户提交的数据保存到数据库
        # 通过ajax发送请求，如果成功了，不嫩返回redirect，要返回一个JSON表示状态是True
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))  # 将python对象转换成json对象，生成的是字符串
    else:
        error = form.errors  # form.errors包含了全部的错误信息，as_json将错误信息转化为json格式
        # 通过ajax发送请求，如果失败了，不嫩返回redirect，要返回一个JSON表示状态是True
        print(error)
        data_dict = {"status": False, "error": error}
        return HttpResponse(json.dumps(data_dict))

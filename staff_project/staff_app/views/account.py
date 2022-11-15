from io import BytesIO

from django import forms
from django.shortcuts import render, HttpResponse, redirect

from staff_app import models
from staff_app.utils.encrypt import md5
from staff_app.utils.bootstrap import BootStrapForm
from staff_app.utils.code import check_code


# 本来这个括号里面应该继承forms.Form,但是utils文件下的bootstrap.py中的BootStrapForm已经继承了forms.Form
class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(),
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(),
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    # 定义一个钩子方法
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """登陆"""
    if request.method == "GET":
        form = LoginForm()  # 实例化我们写的类
        return render(request, "login.html", {"form": form})
    else:
        form = LoginForm(data=request.POST)  # 获取到用户提交的数据
        if form.is_valid():  # 判断是否验证成功
            # 这里是验证码-验证
            user_input_code = form.cleaned_data.pop('code')
            code = request.session.get('image_code', "")
            if code.upper() != user_input_code.upper():
                form.add_error("code", "验证码错误")
                return render(request, 'login.html', {'form': form})

            # 这里是用户名和密码-验证
            # print(form.cleaned_data)  # 验证成功，获取到的用户名和密码
            # 去数据库校验用户名和密码是否正确
            # admin_object = models.Admin.objects.filter(username=form.cleaned_data['username'],password=form.cleaned_data['password']).first()
            # 这里的筛选条件可以是一个字典，我们的form.cleaned_data获取到的就是用户输入的字典，但是需要加上连个**
            admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
            if not admin_object:  # 如果是空，就不是一个对象，是none
                form.add_error("password", "用户名或密码错误")  # 主动添加错误
                return render(request, "login.html", {"form": form})
            else:  # 用户名和密码正确
                # 网站生成随机字符串，写到用户浏览器的cookie中，再写入到网站的session中
                # request.session["info"] = admin_object.username  # 这一步直接完成了生成随机字符串，写到用户浏览器的cookie中，再将用户名写入到网站的session中
                request.session["info"] = {"id": admin_object.id,
                                           "name": admin_object.username}  # 这里写入到网站的session中的info是一个字典，包含id和name
                return redirect("/admin_list/")
        else:
            return render(request, "login.html", {"form": form})  # 验证失败，返回这个，显示错误信息


def image_code(request):
    """ 生成图片验证码 """
    # 调用pillow函数，生成图片
    img, code_string = check_code()
    print(code_string)
    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string

    # 以前我们用脚本产生的图片验证码是张图片，返还到前端还要再读取，很麻烦
    # 现在我们利用 BytesIO() 相当于 内存中的一个对象(可以理解为把图片直接写入内存中)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """注销"""

    request.session.clear()
    return redirect('/login/')

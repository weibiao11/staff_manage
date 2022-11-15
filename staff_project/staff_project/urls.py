"""staff_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from staff_app.views import department, staff, mobile, good, admin, account, task

urlpatterns = [
    # path('admin/', admin.site.urls),

    # 部门管理
    path('department_list/', department.department_list),
    path('department_add/', department.department_add),
    path('department_delete/', department.department_delete),
    path('department_edit/<int:nid>', department.department_edit),
    # 员工管理
    path('staff_list/', staff.staff_list),
    path('staff_add/', staff.staff_add),
    path('modelform_staff_add/', staff.modelform_staff_add),
    path('staff_edit/<int:nid>', staff.staff_edit),
    path('staff_delete/<int:nid>', staff.staff_delete),
    # 靓号管理
    path("mobile_list/", mobile.mobile_list),
    path("mobile_add/", mobile.mobile_add),
    path('mobile_edit/<int:nid>', mobile.mobile_edit),
    path("mobile_delete/<int:nid>", mobile.mobile_delete),
    # 商品管理
    path('good_list/', good.good_list),
    path('good_add/', good.good_add),
    path('good_edit/<int:nid>', good.good_edit),
    path('good_delete/<int:nid>', good.good_delete),
    # 管理员的管理
    path('admin_list/', admin.admin_list),
    path('admin_add/', admin.admin_add),
    path('admin_edit/<int:nid>', admin.admin_edit),
    path('admin_delete/<int:nid>', admin.admin_delete),
    path('admin_reset/<int:nid>', admin.admin_reset),
    # 登录和注销
    path('login/', account.login),
    path('logout/', account.logout),
    path('image_code/', account.image_code),
    # 任务管理
    path('task_list/', task.task_list),
    path('task_ajax/', task.task_ajax),
    path('task_add/', task.task_add),
]

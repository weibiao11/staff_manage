from django.db import models


class Admin(models.Model):
    """管理员"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    # 这是我们用ForeignKey关联表的时候，他显示的是一个对象，我们使用了这个就能让他显示我们的username
    def __str__(self):
        return self.username


class Department(models.Model):
    """部门表"""                """verbose_name：对这一列经行注解"""
    title = models.CharField(verbose_name="部门标题", max_length=32)

    # 这是我们用ForeignKey关联表的时候，他显示的是一个对象，我们使用了这个就能让他显示我们的title
    def __str__(self):
        return self.title


class StaffInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    salary = models.DecimalField(verbose_name="工资", max_digits=8, decimal_places=2, default=0)
    # entry_time = models.DateTimeField(verbose_name="入职时间")
    entry_time = models.DateField(verbose_name="入职时间")
    # to="Department"：与哪个表关联，，to_field="id"：与表中的哪一列关联
    # 在使用Foreignkey时，staff_depart在数据库生成的时候，会自动变为staff_department_id
    # on_delete=models.CASCADE,当部门表被删除，员工表与之相关的全部删除
    # null = True, blank = True,表允许为空，on_delete=models.SET_NULL，当部门表被删除，员工表与之相关的全部置空
    staff_department = models.ForeignKey(verbose_name="所属部门", to="Department", to_field="id", null=True, blank=True,
                                         on_delete=models.CASCADE)
    gender_choices = ((1, "男"), (2, "女"))  # 在django中做的约束
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class MobileNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=11)  # 后面会对手机号进行正则表达式和搜索，所以这里用CharField
    # 想要允许为空 null=True, blank=True
    price = models.IntegerField(verbose_name="价格", default=0)
    # 靓号级别
    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)  # default=1 : 默认为 1

    status_choices = (
        (1, "已占用"),
        (2, "未使用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class GoodInfo(models.Model):
    name = models.CharField(verbose_name="商品名称", max_length=8)
    price = models.DecimalField(verbose_name="商品价格", max_digits=5, decimal_places=2, default=0)
    color_choices = (
        (1, "红色"),
        (2, "绿色")
    )
    color = models.SmallIntegerField(verbose_name="商品的颜色", choices=color_choices, default=1)


class Task(models.Model):
    """任务"""
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时")
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")
    # on_delete=models.CASCADE级联删除
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)

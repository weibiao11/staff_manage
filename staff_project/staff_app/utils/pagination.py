"""

自定义的分页组件，以后如果想要使用这个分页组件，你需要做如下几件事

【在视图函数中】
def mobile_list(request):
    """"""
    # 1:根据自己的情况取筛选自己的数据
    queryset = models.MobileNum.objects.filter(**data_dict).order_by("-level")
    
    # 2：实例化分页对象
    page_object = Pagination(request, queryset,page_size=4)  # 实例化我们自定义的类

    context = {
        "queryset": page_object.page_queryset,   # 分完页的数据
        "page_string": page_object.html()        # 生成的页码
    }
    return render(request, 'mobile_list.html', context)

【在html页面中】
{% for obj in queryset %}
    <tr>
        <th>{{ obj.id }}</th>
        <td>{{ obj.mobile }}</td>
        <td>{{ obj.price }}</td>
        <td>{{ obj.get_level_display }}</td>
        <td>{{ obj.get_status_display }}</td>
        <td>
            <a class="btn btn-primary btn-xs" href="/mobile_edit/{{ obj.id }}">编辑</a>
            <a class="btn btn-danger btn-xs" href="/mobile_delete/{{ obj.id }}">删除</a>
        </td>
    </tr>
{% endfor %}

<ul class="pagination">
    {{page_string}}
</ul>


【参数说明】
request:请求的对象
query:符合条件的数据（根据这个数据给他进行分页处理）
page_size:每页显示多少条数据
page_param:在url中传递的获取的参数，例如/?page=10
plus:显示当前页数的前5页或者后5页，数值可以该，plus=5



【存在小bug】
在搜索+分页的情况下【已解决】
在输入页码跳转页面时
"""
from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):

        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        page = request.GET.get(page_param, "1")  # 获取当前页
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size  # 将其封装进来

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()

        total_page_count, div = divmod(total_count, page_size)
        if div > 0:
            total_page_count = total_page_count + 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 计算出当前页的前5页和后5页
        plus = 5
        # 当页数小于11页时
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            # 当页数小于5时
            if self.page <= plus:
                start_page = 1
                end_page = 2 * plus + 1
            # 当页数大于5时
            else:
                # 当页数+5>总页码时
                if self.page + 5 > self.total_page_count:
                    start_page = self.total_page_count - 2 * plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - plus
                    end_page = self.page + plus + 1

        # 页码
        page_str_list = []

        # 首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            pre = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())  # format里面的值会放入{}中
        else:
            self.query_dict.setlist(self.page_param, [1])
            pre = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(pre)

        # 页面
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())  # format里面的值会放入{}中
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            next = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(next)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        # 跳转页面
        jump_page = """
           <li>
               <form method="get" style="float:left;margin-left:110px;">
                   <div class="input-group" style="width:300px;">
                       <input type="text" name="page" class="form-control" placeholder="请输入要跳转的页码">
                       <span class="input-group-btn">
                           <button class="btn btn-default" type="submit">跳转</button>
                       </span>
                   </div>
               </form>
           </li>
        """

        page_str_list.append(jump_page)

        page_string = mark_safe("".join(page_str_list))
        return page_string

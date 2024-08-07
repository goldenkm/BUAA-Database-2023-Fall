"""
自定义的分页组件，使用步骤：
1、在视图函数中：
    def xxx_list(request):
        # 根据自己的情况去筛选数据
        query_set = models.Department.objects.filter(**data_dict)

        # 实例化分页对象
        page = Pagination(request, queryset=, ...)

        context = {
            "queryset": page.page_queryset,         # 分完页的数据
            "page_string": page.html()              # 生成页码
        }

2、在HTML页面中
    {% for item in queryset %}
        {{item.xx}}
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>
"""
from django.utils.safestring import mark_safe
import copy


class Pagination(object):
    def __init__(self, request, queryset, page_param="page", page_size=10, plus=5):
        """
        :param request: 请求的对象
        :param queryset: 待分页的符合条件的数据
        :param page_param: 每页显示多少条数据
        :param page_size: 在URL中传递的获取分页的参数
        :param plus: 显示当前的 前或后几页
        """
        query_dict = copy.deepcopy(request.GET)
        query_dict.mutable = True
        self.query_dict = query_dict
        self.page_param = page_param
        page = request.GET.get(page_param, '1')
        # 如果得到的是一个十进制数，就转化成整型
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start: self.end]
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if self.page + self.plus > self.total_page_count:
                    start_page = self.page
                    end_page = self.total_page_count + 1
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus
        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 页面
        for i in range(start_page, end_page):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li><a class="is-active" href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next_page = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            next_page = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(next_page)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))
        search_string = """
            <li>
                <form style="float: left; margin-left: -1px" method="get">
                    <input name="page" 
                            style="position: relative; float: left; display: inline-block; width: 80px; border-radius: 0;"
                            type="text" class="input" placeholder="页码">
                    <button style="border-radius: 0" class="button" type="submit">跳转</button>
                </form>
            </li>
        """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect

# 例子:
# class M1(MiddlewareMixin):
#     """中间键"""
#
#     # 如果方法中没有返回值，则继续往后走，
#     # 如果有返回值，HttpResponse,render,redirect则不在继续往后执行，而是把返回值直接呈现给用户的页面
#     def process_request(self,request):
#         print("M1.进来了")
#         return HttpResponse("无权访问")
#
#     def process_response(self,request,response):
#         print("M1.走了")
#         return response
#
#
# class M2(MiddlewareMixin):
#     """中间键"""
#
#     def process_request(self, request):
#         print("M2.进来了")
#
#     def process_response(self, request, response):
#         print("M2.走了")
#         return response


class AuthMiddleware(MiddlewareMixin):
    """中间键"""

    def process_request(self, request):

        # 排除那些不需要中间件判定(登录)就能访问的页面
        if request.path_info in ["/login/", "/img_code/"]:
            return None  # return None,可以直接往后走

        info_dict = request.session.get("info")
        if info_dict:
            return None
        else:
            return redirect('/login/')

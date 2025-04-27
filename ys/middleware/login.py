from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from app01.models import User
import re


class M1(MiddlewareMixin):
    ''' 中间件 '''
    def process_request(self, request):
        # print(request.path_info)
        # if request.path_info == '/app01/login/' or request.path_info == '/app01/user/add/':
        #     return
        if request.path_info == '/':
            return redirect('/play/index/')
        if not re.findall(r'^/ys/', request.path_info):
            return
        info = request.session.get('info')
        # print(info)
        if not info:
            if re.findall(r'^/ys/article/', request.path_info):
                return redirect('/play/'+request.path_info.split('/ys/')[-1])
            return redirect('/app01/login/')
        result2 = User.objects.filter(**info)
        if len(result2) != 1:
            return redirect('/app01/login/')
        return

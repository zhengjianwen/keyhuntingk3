import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class ValidPermission(MiddlewareMixin):

    def process_request(self, request):

        # 当前访问路径
        current_path = request.path_info

        # 检查是否属于白名单
        vaild_url_list = ["/login/", "/reg/", "/admin/.*"]

        for vaild_url in vaild_url_list:
            # 用正则匹配权限的路径和当前路径是否匹配
            ret = re.match(vaild_url, current_path)
            if ret:
                return None

        # 校验是否登录
        # 在session表中取user_id
        user_id = request.session.get("user_id")

        if not user_id:
            return redirect("/login/")

        # # 校验权限1(permission_list)
        # # 在session表中取权限列表(permission_list)
        # permissiion_list = request.session.get("permission_list", [])  # ['/users/', '/users/add', '/users/delete/(\\d+)', 'users/edit/(\\d+)']
        #
        # flag = False
        # for permissiion in permissiion_list:
        #
        #     # 拼接以permissiion开头和结尾，锁定，可以用正则匹配
        #     permissiion = "^%s$" % permissiion
        #
        #     ret = re.match(permissiion, current_path)
        #     if ret:
        #         flag = True
        #         break
        # if not flag:
        #     return HttpResponse("没有访问权限！")
        #
        # return None

        # 校验权限2
        permissions_dict = request.session.get("permissions_dict")
        print(permissions_dict)

        for item in permissions_dict.values():
            urls = item["urls"]
            for reg in urls:
                reg = "^%s$" % reg
                ret = re.match(reg, current_path)
                if ret:
                    print("actions", item["action"])
                    request.actions = item['action']
                    return None

        return HttpResponse("没有访问权限！")

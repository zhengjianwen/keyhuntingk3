def initial_session(user, request):

    # # 方案一：
    #
    # # distinct()去重
    # # 去重取到所有角色
    # permissions = user.roles.all().values("permissions__url").distinct()
    #
    # permission_list = []
    #
    # for item in permissions:
    #     permission_list.append(item["permissions__url"])
    # print(permission_list)
    #
    # # 给session设置权限列表(permission_list)
    # request.session["permission_list"] = permission_list


    # 方案二：
    permissions = user.roles.all().values("permissions__url", "permissions__group_id", "permissions__action").distinct()
    print("permissions", permissions)

    permissions_dict = {}
    for item in permissions:
        gid = item.get("permissions__group_id")

        if not gid in permissions_dict:

            permissions_dict[gid] = {
                "urls": [item["permissions__url"],],
                "action": [item["permissions__action"],]
            }
        else:
            permissions_dict[gid]["urls"].append(item["permissions__url"])
            permissions_dict[gid]["action"].append(item["permissions__action"])

    print(permissions_dict)
    request.session["permissions_dict"] = permissions_dict


    # 注册菜单权限
    permissions = user.roles.all().values("permissions__url", "permissions__action", "permissions__group__title").distinct()
    print("permissions", permissions)

    menu_permission_list = []
    for item in permissions:
        if item["permissions__action"] == "list":
            menu_permission_list.append((item["permissions__url"], item["permissions__group__title"]))

    print(menu_permission_list)
    request.session["menu_permission_list"] = menu_permission_list

import xlrd
import os
import uuid
from app01 import path
from .models import *
from django.views import View
from app01 import models
from django.shortcuts import render


class Index(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        """
        读取excel表格信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        ret = {"code": 1000, "data": None}

        try:
            print(111111111111)
            # 获取文件
            a = request.POST.get('aaa')
            print(a)
            files = request.FILES.get('code')
            print(22222222222222,  files)
            print(files.name)
            # 检查文件后缀名
            name_after = files.name.rsplit('.', maxsplit=1)[1]
            print(name_after)
            if name_after == 'xls':
                with open(files.name, 'wb+') as f:
                    for chunk in files.chunks():
                        f.write(chunk)
                data = xlrd.open_workbook('伊犁型材.xls')
                print(data)
                # 通过索引顺序获取
                worksheet1 = data.sheets()[0]
                print(worksheet1)

                # 遍历sheet1中所有行row
                num_rows = worksheet1.nrows
                print(num_rows)
                for curr_row in range(num_rows):
                    row = worksheet1.row_values(curr_row)
                    # print('row%s is %s' % (curr_row, row))
                    for n in row:
                        if n == '':
                            row.remove(n)
                    print(row)

                    li = []
                    # li.append(models.Userinfo.objects.filter(date=row[1]).first())
                    li.append(models.Userinfo.objects.filter(status=row[3]).first())
                    li.append(models.Userinfo.objects.filter(name=row[6]).first())
                    li.append(models.Userinfo.objects.filter(num=row[8]).first())

                    for i in li:
                        if i == '':
                            ret['code'] = 1003
                            ret['error'] = '读取数据和数据库不一致'
            else:
                ret['code'] = 1002
                ret['error'] = '不是excel文件'
        except Exception as e:
            ret['code'] = 1001
            ret['error'] = '获取信息不一致'

        return render(request, 'index.html', {'ret': ret})


# def func(request):
#     res = {'state': False}
#     data = xlrd.open_workbook(path.a)
#     table = data.sheets()[0]
#     nrows = table.nrows
#     for i in range(nrows):
#         if i == 0:
#             continue
#         # print(table.row_values(i))
#         if table.row_values(i)[6] == '伊犁蓝山屯河型材有限公司':
#             name = Userinfo.objects.filter(name=table.row_values(i)[6]).first()
#             print(name)
#             res['state'] = 100
#             print(res)
#     return render(request, 'index.html', {'res': res})


from django.shortcuts import render, redirect
import xlrd
from app01 import path
from .models import *


def func(request):
    res = {'state': False}
    data = xlrd.open_workbook(path.a)
    table = data.sheets()[0]
    nrows = table.nrows
    for i in range(nrows):
        if i == 0:
            continue
        # print(table.row_values(i))
        if table.row_values(i)[6] == '伊犁蓝山屯河型材有限公司':
            name = Userinfo.objects.filter(name=table.row_values(i)[6]).first()
            print(name)
            res['state'] = 100
            print(res)
    return render(request, 'index.html', {'res': res})


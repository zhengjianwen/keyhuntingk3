import xlrd
from django.views import View
from app01 import models
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import *
from django import forms
from django.forms import widgets
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


# 登陆
def login(request):

    # 判断是否走ajax请求
    if request.is_ajax():

        # 获取用户名、密码和验证码信息
        username = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code = request.POST.get("valid_code")

        # 设置个传给ajax的state状态和msg信息
        res = {"state": False, "msg": None}

        # 拿着浏览器的cookie的随机字符，在dhango的session表里的session_id中，取session_data中的valid_str值
        valid_str = request.session.get("valid_str")

        if valid_code.upper() == valid_str.upper():
            user = User.objects.filter(username=username, password=pwd).first()
            if user:
                res["state"] = True
                request.session['username'] = username
            else:
                # 返回用户名或密码错误信息
                res["msg"] = "userinfo or pwd error"
        else:
            # 返回验证码错误信息
            res["msg"] = "验证码错误"
        # django序列化后传给前端的res信息
        return JsonResponse(res)

    return render(request, "login.html")


# 生成图片验证码
def get_valid_img(request):

    # 方式：
    # 生成Image图片
    from PIL import Image
    # 图像画柄和字体设置相关
    from PIL import ImageDraw, ImageFont
    import random

    # 随机颜色函数
    def get_random_color():
        return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

    # 生成一个原始图片
    image = Image.new("RGB", (250, 40), get_random_color())

    # 给Image图片添加东西
    draw = ImageDraw.Draw(image)

    # 设置字体
    # truetype参数("字体样式的路径","字体大小")
    font = ImageFont.truetype("static/font/kumo.ttf", size=32)

    # 生成五个随机字符
    temp = []
    for i in range(5):
        random_num = str(random.randint(0,9))
        random_low_alpha = chr(random.randint(97, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])

        # 往这个图片中添加文字
        # text的参数("坐标点","放入的文字", "字体颜色", "字体样式")
        draw.text((24+i*36, 0), random_char, get_random_color(), font=font)

        # 保存随机字符
        temp.append(random_char)

    # 噪点噪线
    # width=250
    # height=40
    # for i in range(100):
    #     x1=random.randint(0,width)
    #     x2=random.randint(0,width)
    #     y1=random.randint(0,height)
    #     y2=random.randint(0,height)
    #     # 往这个图片中画线
    #     draw.line((x1,y1,x2,y2),fill=get_random_color())
    #
    # for i in range(400):
    #     # 往这个图片中画点
    #     draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    # 在内存生成图片
    from io import BytesIO
    # BytesIO实例化
    f = BytesIO()
    # 保存图片
    image.save(f, "png")

    # 把图片的内容赋值给data
    data = f.getvalue()
    f.close()

    valid_str = "".join(temp)
    print("valid_str", valid_str)

    # 当浏览器第一次访问网页,给session表中添加一条session记录，如果有这条记录，下一次访问，就在session表中session_data信息覆盖更新
    # 当浏览器访问网页cookie随机字符,给session表中session_data中设置valid_str的值
    request.session["valid_str"] = valid_str

    return HttpResponse(data)


# 用form组件创建注册表单
class RegForm(forms.Form):

    user = forms.CharField(max_length=8, label="用户名", widget=widgets.TextInput(attrs={"class": "form-control"}))
    pwd = forms.CharField(min_length=4, label="密码", widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    repeat_pwd = forms.CharField(min_length=4, label="确认密码", widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="邮箱", widget=widgets.EmailInput(attrs={"class": "form-control"}))

    def clean_user(self):
        val = self.cleaned_data.get("user")

        ret = User.objects.filter(username=val)

        if not ret:
            return val
        else:
            raise ValidationError("该用户已经不存在")

    def clean(self):
        if self.cleaned_data.get("pwd") == self.cleaned_data.get("repeat_pwd"):
            return self.cleaned_data
        else:
            raise ValidationError("两次密码不一致！")


# 注册
def reg(request):
    # 判断是够走POST请求
    if request.method == "POST":
        res = {"user": None, "error_dict": None}
        form = RegForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)  # {"user":"yuan","pwd":"12345","repeat_pwd":"12","email":"123"}
            print(request.FILES)

            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar = request.FILES.get("avatar")
            print("user", user)

            if avatar:
                user = User.objects.create(username=user, password=pwd, email=email, avatar=avatar)
            else:
                user = User.objects.create(username=user, password=pwd, email=email)

            res["user"] = user.username
        else:
            print(form.errors)   # {"repeat_pwd":["....",],"email":["......",]}
            print(form.cleaned_data)
            res["error_dict"] = form.errors
        return JsonResponse(res)

    form = RegForm()
    return render(request, "reg.html", locals())


class Index(View):
    def get(self, request, *args, **kwargs):
        # 通过session，判断用户表中的username是否存在
        if not request.session.get('username'):
            return redirect("/login/")
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
            # 获取文件
            files = request.FILES.get('code')
            # 检查文件后缀名
            name_after = files.name.rsplit('.', maxsplit=1)[1]
            print(name_after)
            if name_after == 'xls':
                with open(files.name, 'wb+') as f:
                    for chunk in files.chunks():
                        f.write(chunk)
                data = xlrd.open_workbook('伊犁型材.xls')
                # 通过索引顺序获取
                worksheet1 = data.sheets()[0]

                # 遍历sheet1中所有行row
                num_rows = worksheet1.nrows
                print(num_rows)
                for curr_row in range(num_rows):
                    row = worksheet1.row_values(curr_row)
                    # print('row%s is %s' % (curr_row, row))
                    for n in row:
                        if n == '':
                            row.remove(n)
                    li = []
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


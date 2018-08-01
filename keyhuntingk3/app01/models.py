from django.db import models


# 信息
class Userinfo(models.Model):
    """
    信息
    """
    date = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    name = models.CharField(verbose_name='公司名称', max_length=64)
    status = models.CharField(verbose_name='入库状态', max_length=64)
    num = models.CharField(verbose_name='编码', max_length=64)

    def __str__(self):
        return self.name


class User(models.Model):
    """
    用户详情
    """
    telephone = models.CharField(max_length=11, null=True, unique=True)
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='用户密码', max_length=32)
    email = models.CharField(verbose_name='邮箱', max_length=64)
    avatar = models.FileField(upload_to='avatars/', default="/avatars/default.png")

    def __str__(self):
        return self.username

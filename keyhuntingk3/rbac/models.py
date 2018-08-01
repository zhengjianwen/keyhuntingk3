from django.db import models

# Create your models here.


# 用户表
class User(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    roles = models.ManyToManyField(to="Role")

    def __str__(self): return self.name


# 角色表
class Role(models.Model):
    title = models.CharField(max_length=32)
    permissions = models.ManyToManyField(to="Permission")

    def __str__(self): return self.title


# 权限表
class Permission(models.Model):
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=1024)

    action = models.CharField(max_length=32, default="")
    group = models.ForeignKey(to="PermissionGroup", default=1)

    def __str__(self): return self.title


# 分组表
class PermissionGroup(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self): return self.title

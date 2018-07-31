from app01 import models
from rest_framework import serializers


class ExcelSerializer(serializers.ModelSerializer):
    """
    excel信息序列化
    """

    date = serializers.CharField(source='userinfo.date')
    name = serializers.CharField(source='userinfo.name')
    status = serializers.CharField(source='userinfo.status')
    num = serializers.CharField(source='userinfo.num')

    class Meta:
        models = models.Userinfo
        fields = ['date', 'name', 'status', 'num']


# -*- coding: utf-8 -*-
# __author__ = 'Aston'
from rest_framework import permissions

# 这个类用来说明一个病人记录只能够被自己的医生所访问，用来避免客户端在拥有ID的情况下错误的操作
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 现在还不确定obj是否有owner这个参数，还是用doctor_id？
        # 因为当前的doctor_id并没有与User库关联起来。
        # print(obj.owner);
        # Any permissions are only allowed to the owner of the patient.
        return obj.doctor_id == request.user
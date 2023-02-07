# -*- coding : utf-8 -*-            
# @Time : 2022/5/1 13:20
# @Author : SXQ
# @FileName : encrypt
import hashlib
from django.conf import settings


def md5(data_string):
    # 加言
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()

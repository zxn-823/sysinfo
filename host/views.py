from django.shortcuts import render
import os
import platform
from datetime import datetime
import time
import psutil

# Create your views here.
# 需求1: 用户访问http://127.0.0.1:8000,返回主机的详情信息
def index(request):
    try:
        # 如果是Linux系统,执行下面内容
        # os.uname在windows系统中不能执行
        system_info = os.uname()
        node = system_info.nodename
        system = system_info.sysname
    except Exception as e:
        # 如果是Windows系统,执行下面内容
        system_info = platform.uname()
        node = system_info.node
        system = system_info.system

    boot_time = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time)
    now_time = datetime.fromtimestamp(time.time())
    info = {
        'node':node,
        'system': system,
        'kernal_name': system,
        'release': system_info.release,
        'version': system_info.version,
        'machine': system_info.machine,
        'now_time': now_time,
        'boot_time': boot_time,
        'boot_delta': now_time-boot_time


    }
    return render(request,'host/index.html',{'info': info})




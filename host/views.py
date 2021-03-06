import difflib

from django.shortcuts import render
from django.http import HttpResponse
import os
import platform
from datetime import datetime
import time
import psutil

# Create your views here.
# 需求1: 用户访问http://127.0.0.1:8000,返回主机的详情信息
from host.tools import get_md5


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

# 需求2:用户访问http://ip/disk/,返回磁盘分区的详细信息
def disk(request):
    # 获取系统所有的磁盘分区
    parts = psutil.disk_partitions()
    disks = []
    # 依次遍历获取每个分区的详细信息
    for part in parts:
        # 查看当前磁盘分区的使用率
        usage = psutil.disk_usage(part.device)
        # 每个分区的详细信息存储到列表中
        disk = {
            'device':part.device,
            'mountpoint':part.mountpoint,
            'fstype':part.fstype,
            'opts':part.opts,
            'total':usage.total,
            'percent':usage.percent,
        }
        disks.append(disk)
    # 返回html页面信息
    return render(request,'host/disk.html',{'disks':disks})

# 需求3：用户访问http://ip/users/,返回当前登录用户的详细信息
def users(request):
    all_users = []
    users = psutil.users()
    for user in users:
        one_user = {
            'name':user.name,
            'host':user.host,
            'started':datetime.fromtimestamp(user.started)
        }
        all_users.append(one_user)
    return render(request,'host/users.html',{'users':all_users})

# 需求4：用户访问http://ip/, diff/,返回html页面，可以让用户上传文件
def diff(request):
    """
    HTTP请求方法有哪些?
        - GET: 一般情况下Get方法用于获取html页面内容
        - POST: 一般情况下用于上传数据信息和上传文件信息
    """
    print("客户端请求的方法: ", request.method)
    if request.method == 'POST':
        # 获取用户前端上传的文件
        files = request.FILES
        # 获取第一个和第二个文件对象, 通过read读取文件的内容
        content1 = files.get('filename1').read()
        content2 = files.get('filename2').read()
        # 对于文件进行差异性对比
        # 判断md5加密是否相同， 如果相同，则文件一致，否则，显示差异性对比
        # 如何自动导入模块? Alt+Enter
        if get_md5(content1) == get_md5(content2):
            return HttpResponse("文件内容一致")
        else:
            hdiff = difflib.HtmlDiff()
            content1 = content1.decode('utf-8').splitlines()
            content2 = content2.decode('utf-8').splitlines()
            # print(content1)
            # make_file传入的是列表类型的文件内容
            result = hdiff.make_file(content1, content2)  # 会生成一个html字符串
            return HttpResponse(result)
    return render(request, 'host/diff.html')
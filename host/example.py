"""
主机名:
操作系统:
内核名称:
发行版本号:
内核版本
系统架构
当前时间
开机时间
开机时长
"""
# os模块, operate system, 跟操作系统相关的方法, 多是文件操作等
import os
import  platform
from datetime import  datetime
import  time
try:
    # os.uname在windows系统中不能执行
    system_info = os.uname()
except Exception as e:
    system_info = platform.uname()

import psutil
boot_time = psutil.boot_time()
boot_time =  datetime.fromtimestamp(boot_time)
now_time =  datetime.fromtimestamp(time.time())

print("""
***********************************主机信息监控********************************
        主机名: %s
        操作系统: %s
        内核名称: %s
        发行版本号: %s
        内核版本: %s
        系统架构: %s
        当前时间: %s
        开机时间: %s
        开机时长: %s
""" %(system_info.nodename, system_info.sysname, system_info.sysname,
      system_info.release, system_info.version, system_info.machine,
      now_time, boot_time, now_time-boot_time
      ))

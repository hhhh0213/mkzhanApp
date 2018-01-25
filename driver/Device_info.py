# coding: utf-8

import re
import subprocess


def connectDevice():
    # 检查设备是否连接成功，如果成功返回True，否则返回False
    try:
        '''获取设备列表信息，并用"\r\n"拆分'''
        deviceInfo = subprocess.check_output('adb devices', shell=True)
        '''如果没有链接设备或者设备读取失败，第二个元素为空'''
        if deviceInfo[25] == '\n':
            return False
        else:
            return True
    except Exception, e:
        print "Device Connect Fail:", e


def getAndroidVersion():
    try:
        if connectDevice():
            # 获取系统设备系统信息
            sysInfo = subprocess.check_output('adb shell cat /system/build.prop', shell=True)
            # 获取安卓版本号
            androidVersion = re.findall("version.release=(\d\.\d\.\d)*", sysInfo, re.S)[0]
            return androidVersion
        else:
            return "Connect Fail,Please reconnect Device..."
    except Exception, e:
        print "Get Android Version:", e


def getDeviceName():
    try:
        if connectDevice():
            # 获取设备名
            deviceInfo = subprocess.check_output('adb devices -l', shell=True)
            deviceName = re.findall(r'product:(.*)\smodel', deviceInfo, re.S)[0]
            return deviceName
        else:
            return "Connect Fail,Please reconnect Device..."
    except Exception, e:
        print "Get Device Name:", e



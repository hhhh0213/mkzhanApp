# -*- coding:utf-8 -*-

from appium import webdriver
from driver import Device_info

appPackage = 'com.xmtj.mkz'
appActivity = '.StartActivity'

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = Device_info.getAndroidVersion()
desired_caps['deviceName'] = Device_info.getDeviceName()
desired_caps['appPackage'] = appPackage
desired_caps['appActivity'] = appActivity
desired_caps['noReset'] = 'true'
desired_caps["resetKeyBoard"] = True
desired_caps['unicodeKeyboard'] = True


def AppiumStart(self):
    self.desired_caps = desired_caps
    self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

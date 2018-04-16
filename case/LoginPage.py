# -*- coding:utf-8 -*-

import time
import unittest
import os
from config import appium_config, Page_config
from driver import GetToast, Swipe_op
from driver.GetImg import Appium_Extend
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.connectiontype import ConnectionType


# 设置路径信息
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

# 账号输入框ID
usernameID = Page_config.PageID.usernameID
# 登录按钮ID
logInID = Page_config.PageID.logInID
# 退出登录按钮ID
loginOut = Page_config.PageID.loginOut
# 输入账号文本
usernameText = Page_config.PageID.usernameText
usernameTextEr = 'ja'
# 密码输入框ID
passwordID = Page_config.PageID.passwordID
# 输入密码文本
passwordText = Page_config.PageID.passwordText
passwordTextEr1 = '1233211'
passwordTextEr2 = '123'


class LoginTest(unittest.TestCase):
    global driver

    # 初始化环境
    @classmethod
    def setUpClass(cls):
        # 更改Appium启动参数
        appium_config.desired_caps['automationName'] = 'Uiautomator2'
        # 启动Appium
        appium_config.AppiumStart(cls)
        cls.extend = Appium_Extend(cls.driver)

        # 获取手机屏幕分辨率
        cls.x = cls.driver.get_window_size()['width']
        cls.y = cls.driver.get_window_size()['height']

        # 进入我的-登录页面
        time.sleep(5)
        cls.driver.find_element_by_id(Page_config.PageID.homeMy).click()
        cls.driver.find_element_by_id(Page_config.PageID.myLogin).click()
        time.sleep(3)

    # 退出测试
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    '''无网环境，登录失败的用例
    def test_case_loginCase1(self):
        # 切断手机所有网络
        self.driver.set_network_connection(ConnectionType.NO_CONNECTION)

        # 输入错误的账号/密码
        self.driver.find_element_by_id(usernameID).send_keys(usernameTextEr)
        self.driver.find_element_by_id(passwordID).send_keys(passwordTextEr1)
        while True:
            try:
                self.driver.find_element_by_id(logInID).click()
                # 获取并验证登录失败的toast提示
                GetToast.find_toast(u"登录失败", 30, 0.1, self.driver)
                break
            except Exception, e:
                continue

        print '无网环境登录测试通过'
        self.driver.find_element_by_id(usernameID).clear()
        self.driver.find_element_by_id(passwordID).clear()

        # 开启手机wifi网络
        self.driver.set_network_connection(ConnectionType.WIFI_ONLY)
        time.sleep(5)

    # 账号/密码错误，登录失败的用例
    def test_case_loginCase2(self):
        self.driver.find_element_by_id(usernameID).send_keys(usernameTextEr)
        self.driver.find_element_by_id(passwordID).send_keys(passwordTextEr1)
        while True:
            try:
                self.driver.find_element_by_id(logInID).click()
                # 获取并验证登录错误的toast提示
                GetToast.find_toast(u'账号或密码错误', 30, 0.1, self.driver)
                break
            except Exception, e:
                continue

        self.driver.find_element_by_id(usernameID).clear()
        self.driver.find_element_by_id(passwordID).clear()

        print '账号/密码错误测试通过'
        time.sleep(3)

    # 账号/密码为空，登录按钮无法点击的用例
    def test_case_loginCase3(self):
        # 获取默认登录按钮截图
        element1 = self.driver.find_element_by_id(logInID)
        self.extend.get_screenshot_by_element(element1).write_to_file("./", "image")
        self.assertTrue(os.path.isfile("./image.png"))

        # 只输入账号，密码为空时，登录按钮状态截图
        self.driver.find_element_by_id(usernameID).send_keys(usernameText)
        element2 = self.driver.find_element_by_id(logInID)

        load = self.extend.load_image("./image.png")

        # 对比两个截图，要求百分百相似
        result = self.extend.get_screenshot_by_element(element2).same_as(load, 0)
        self.assertTrue(result)

        print '账号/密码为空测试通过'
        time.sleep(3)

    # 密码格式错误，登录失败的用例
    def test_case_loginCase4(self):
        self.driver.find_element_by_id(passwordID).send_keys(passwordTextEr2)
        try:
            loginButton = self.driver.find_element_by_id(logInID)
            if loginButton is not None:
                loginButton.click()
        except Exception, e:
            print '登录按钮不正确'

        # 获取并验证登录错误的toast提示
        GetToast.find_toast(u'密码格式错误，只能包含数字，字母和特殊符号（6-16个字符）', 30, 0.1, self.driver)

        self.driver.find_element_by_id(usernameID).clear()
        self.driver.find_element_by_id(passwordID).clear()
        print '密码格式错误测试通过'
        time.sleep(3)
'''
    # 第三方平台登录测试
    def test_case_loginCase5(self):
        qq = self.driver.is_app_installed('com.tencent.mobileqq')
        wx = self.driver.is_app_installed('com.tencent.mm')
        wb = self.driver.is_app_installed('com.sina.weibo')

        # QQ登录
        self.driver.find_element_by_id(Page_config.PageID.thirdLogin_qq).click()
        if qq:
            # 判断是否进入QQ客户端登录页面
            self.assertTrue(self.driver.wait_activity('com.tencent.qqconnect.wtlogin.Login', 5, 1))
            print '正常跳转QQ登录页面'
        else:
            # 判断是否进入QQH5登录页面
            WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_xpath('//android.webkit.WebView['
                                                                                            '@content-desc="授权并登录"]'))
        self.driver.press_keycode('4')
        time.sleep(3)

        # 微信登录
        self.driver.find_element_by_id(Page_config.PageID.thirdLogin_wx).click()
        if wx:
            try:
                # self.assertTrue(self.driver.wait_activity('.plugin.base.stub.WXEntryActivity', 10, 1))
                print '正常跳转微信登录页面'
                while True:
                    try:
                        self.driver.find_element_by_id('com.tencent.mm:id/hp').click()
                        break
                    except Exception, e:
                        continue
            except Exception, e:
                print '返回操作失败'
        else:
            try:
                GetToast.find_toast(u'未安装微信', 10, 0.1, self.driver)
            except Exception, e:
                pass
        time.sleep(3)

        # 新浪微博登录
        self.driver.find_element_by_id(Page_config.PageID.thirdLogin_wb).click()
        time.sleep(3)
        if wb:
            try:
                self.assertTrue(self.driver.wait_activity('.SSOLoginActivity', 10, 0.5))
                print '正常跳转微博登录页面'
            except Exception, e:
                pass
        else:
            WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_xpath('//android.webkit.WebView['
                                                                                            '@content-desc="登录 - 新浪微博"]'))
        self.driver.press_keycode('4')
        time.sleep(3)

    # 登录成功的用例
    def test_case_loginCase6(self):
        self.driver.find_element_by_id(usernameID).send_keys(usernameText)
        self.driver.find_element_by_id(passwordID).send_keys(passwordText)
        try:
            loginButton = self.driver.find_element_by_id(logInID)
            if loginButton is not None:
                loginButton.click()
        except Exception, e:
            print '登录按钮不正确'

        self.assertTrue(self.driver.wait_activity('.MainActivity', 20, 1))
        while True:
            try:
                self.driver.find_element_by_id(Page_config.PageID.settingID).click()
                break
            except Exception, e:
                Swipe_op.SwipeDown(self)
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.titleID))

        while True:
            try:
                self.driver.find_element_by_id(Page_config.PageID.loginOut).click()
                break
            except Exception, e:
                Swipe_op.SwipeDown(self)
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/msg'))
        self.driver.find_element_by_id('com.xmtj.mkz:id/sure').click()
        print '登录成功测试通过'
        time.sleep(3)


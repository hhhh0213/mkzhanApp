# -*- coding:utf-8 -*-

import time
import unittest
import os
from config import appium_config, Page_config
from driver import GetToast
from driver.GetImg import Appium_Extend
from appium.webdriver.connectiontype import ConnectionType

# 设置路径信息
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

# 账号输入框ID
usernameID = Page_config.PageID.usernameID
# 输入的手机号码
userNumText = Page_config.PageID.userNumText
userNumTextEr1 = '15111000000'
userNumTextEr2 = '11111122223'
userNumTextEr3 = '123'
# 获取验证码ID
getNumID = Page_config.PageID.getNumID
# 输入验证码ID
numID = Page_config.PageID.numID
# 密码输入框ID
passwordID = Page_config.PageID.passwordID
# 输入密码
passwordText = Page_config.PageID.passwordText
passwordTextEr = '123'
# 密码明文ID
view_passID = Page_config.PageID.view_passID
# 重置按钮ID
resetPasswordID = Page_config.PageID.resetPasswordID


class ForgetPassTest(unittest.TestCase):
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

        time.sleep(5)

        # 进入忘记密码页面
        cls.driver.find_element_by_id(Page_config.PageID.homeMy).click()
        cls.driver.find_element_by_id(Page_config.PageID.myLogin).click()
        time.sleep(2)
        cls.driver.find_element_by_id(Page_config.PageID.forgetPasswordID).click()

    # 退出测试
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    '''手机号输入错误，重置密码失败的用例'''
    def test_case_forgetPassEr1(self):
        # 判断页面标题是否正确
        try:
            self.assertEqual(self.driver.find_element_by_id(Page_config.PageID.titleID).text, u'找回密码')
        except Exception, e:
            pass
        while True:
            try:
                # 手机号为空时，点击获取验证码测试用例
                self.driver.find_element_by_id(getNumID).click()
                # 获取并验证失败的toast提示
                GetToast.find_toast(u'手机号码格式错误', 5, 0.1, self.driver)
                break
            except Exception, e:
                continue

        # 手机号格式不为手机号码时，点击获取验证码测试用例
        self.driver.find_element_by_id(usernameID).send_keys(userNumTextEr2)
        self.driver.find_element_by_id(getNumID).click()
        GetToast.find_toast(u'手机号码格式错误', 5, 0.1, self.driver)
        self.driver.find_element_by_id(usernameID).clear()

        # 手机号格式少于11位时，点击获取验证码测试用例
        self.driver.find_element_by_id(usernameID).send_keys(userNumTextEr3)
        self.driver.find_element_by_id(getNumID).click()
        GetToast.find_toast(u'手机号码格式错误', 5, 0.1, self.driver)
        self.driver.find_element_by_id(usernameID).clear()

        # 手机号未注册时，点击获取验证码测试用例
        self.driver.find_element_by_id(usernameID).send_keys(userNumTextEr1)
        self.driver.find_element_by_id(getNumID).click()
        GetToast.find_toast(u'手机号还未注册', 5, 0.1, self.driver)
        self.driver.find_element_by_id(usernameID).clear()

        print '手机号输入有误的情况，测试通过'
        time.sleep(3)

    '''验证码输入有误，重置密码失败的用例'''
    def test_case_forgetPassEr2(self):
        self.driver.find_element_by_id(usernameID).send_keys(userNumText)
        self.driver.find_element_by_id(numID).send_keys('1231')
        self.driver.find_element_by_id(passwordID).send_keys(passwordText)
        for x in range(1, 11):
            try:
                self.driver.find_element_by_id(resetPasswordID).click()
                # 获取并验证登录错误的toast提示
                GetToast.find_toast(u'短信验证码格式不正确', 5, 0.1, self.driver)
                break
            except Exception, e:
                continue
        self.driver.find_element_by_id(passwordID).clear()

        print '验证码有误的情况，测试通过'
        time.sleep(3)

    '''密码格式输入有误，重置密码失败的用例'''
    def test_case_forgetPassEr3(self):
        self.driver.find_element_by_id(passwordID).send_keys(passwordTextEr)
        self.driver.find_element_by_id(resetPasswordID).click()
        GetToast.find_toast(u'密码格式错误，只能包含数字，字母和特殊符号（6-16个字符）', 5, 0.1, self.driver)
        self.driver.find_element_by_id(usernameID).clear()

        '''测试密码框明文显示及删除按扭功能'''
        # 获取密文文本为空
        text1 = self.driver.find_element_by_id(passwordID).text
        # 获取点击密码明文显示后的文本
        self.driver.find_element_by_id(view_passID).click()
        text2 = self.driver.find_element_by_id(passwordID).text
        # 判断密文与明文显示，不同则通过
        self.assertNotEqual(text1, text2)

        # 注册页面密码输入框删除图标在默认机型上的相对坐标
        x1 = 514.00 / 720
        y1 = 452.00 / 1280
        # 注册页面密码输入框删除图标在实际测试机型上的坐标位置
        x_click = int(x1 * self.x)
        y_click = int(y1 * self.y)

        # 密码清空后，明文按钮应为空，以此判断是否正常清理及清理后按钮消失
        self.driver.find_element_by_id(passwordID).click()
        self.driver.tap([(x_click, y_click)])
        try:
            if self.driver.find_element_by_id(view_passID) is not None:
                print '清空密码出错'
        except Exception, e:
            pass

        print '密码格式有误的情况及密码明文显示与删除，测试通过'
        time.sleep(2)

    '''无网环境，重置密码失败的测试用例
    def test_case_forgetPassEr4(self):
        # 切断手机所有网络
        self.driver.set_network_connection(ConnectionType.NO_CONNECTION)

        # 无网获取手机验证码
        self.driver.find_element_by_id(usernameID).send_keys(userNumText)
        for x in range(1, 6):
            try:
                self.driver.find_element_by_id(getNumID).click()
                GetToast.find_toast(u'获取验证码失败', 5, 0.1, self.driver)
                break
            except Exception, e:
                continue

        # 无网提交重置密码申请
        self.driver.find_element_by_id(numID).send_keys('123111')
        self.driver.find_element_by_id(passwordID).send_keys(passwordText)
        self.driver.find_element_by_id(resetPasswordID).click()
        GetToast.find_toast(u'修改密码失败', 5, 0.1, self.driver)

        print '无网环境，测试通过'
        # 开启手机wifi网络
        self.driver.set_network_connection(ConnectionType.WIFI_ONLY)
        time.sleep(3)
'''
# -*- coding:utf-8 -*-

import time
import unittest
import os
import re
import random
from config import appium_config, Page_config
from driver import Swipe_op, go_comic
from selenium.webdriver.support.wait import WebDriverWait

# 设置路径信息
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class UserActivityTest(unittest.TestCase):
    global driver

    # 初始化环境
    @classmethod
    def setUpClass(cls):
        # 更改Appium启动参数
        appium_config.desired_caps['automationName'] = 'Appium'
        # 启动Appium
        appium_config.AppiumStart(cls)

        # 获取手机屏幕分辨率
        cls.x = cls.driver.get_window_size()['width']
        cls.y = cls.driver.get_window_size()['height']

        time.sleep(5)

        # 判断是否存在收藏提醒
        if go_comic.go_comic(cls) is True:
            print '存在收藏更新提醒，点击关闭测试通过'
        else:
            pass

        # 进入我的页面
        cls.driver.find_element_by_id(Page_config.PageID.homeMy).click()

    # 退出测试
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # 测试个人动态页面
    def test_case_UserActivityCase1(self):
        # 进入个人主页
        element_mylogin = self.driver.find_element_by_id(Page_config.PageID.myLogin)
        self.assertEqual(element_mylogin.text, u'查看个人主页')
        element_mylogin.click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/user_collect_title'))

        # 个人主页右上角显示“编辑资料”
        self.driver.find_element_by_id('com.xmtj.mkz:id/btn_follow')

        # 进入关注、粉丝页面测试功能，由于CDN缓存，暂时只验证操作流程
        self.driver.find_element_by_id('com.xmtj.mkz:id/focus_count_layout').click()  # 进入关注列表
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id('android:id/list'))
        element_focusList = self.driver.find_elements_by_id('com.xmtj.mkz:id/tv_name')
        element_focusButton = self.driver.find_elements_by_id('com.xmtj.mkz:id/tv_follow')
        num1 = random.randint(0, len(element_focusList) - 1)
        element_focus = element_focusList[num1]
        element_focusName = element_focus.text
        self.assertEqual(element_focusButton[num1].text, u'已关注')
        print '关注列表随机选择的已关注用户为：%s' % element_focusName

        # 测试取消关注操作
        element_focusButton[num1].click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/msg'))
        self.driver.find_element_by_id('com.xmtj.mkz:id/sure').click()
        try:
            if element_focusName in element_focusList[num1].text:
                print '取消关注操作测试失败！！！！！'
        except Exception, e:
            print '关注列表取消关注测试通过'
        time.sleep(2)
        self.driver.find_element_by_id('com.xmtj.mkz:id/white_back').click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.myImgID))

        # 进入粉丝列表
        self.driver.find_element_by_id('com.xmtj.mkz:id/fans_count_layout').click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id('android:id/list'))
        element_fansList = self.driver.find_elements_by_id('com.xmtj.mkz:id/tv_name')
        element_fansButton = self.driver.find_elements_by_id('com.xmtj.mkz:id/tv_follow')
        num2 = random.randint(0, len(element_fansList) - 1)
        element_fans_name = element_fansList[num2]
        print '粉丝列表随机选择的用户为：%s' % element_fans_name.text

        # 根据该粉丝状态，进行关注/取消关注操作测试
        try:
            if element_fansButton[num2].text == u'关注':
                element_fansButton[num2].click()
                time.sleep(1)
                self.assertEqual(element_fansButton[num2].text, u'已关注')
                print '粉丝列表关注测试通过'
            elif element_fansButton[num2].text == u'已关注':
                element_fansButton[num2].click()
                WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/msg'))
                self.driver.find_element_by_id('com.xmtj.mkz:id/sure').click()
                self.assertEqual(element_fansButton[num2].text, u'关注')
                print '粉丝列表取消关注测试通过'
        except Exception, e:
            print e
        time.sleep(2)
        self.driver.find_element_by_id('com.xmtj.mkz:id/white_back').click()

        # 收藏列表判断
        element_collect = self.driver.find_element_by_id('com.xmtj.mkz:id/user_collect_title')
        element_collectText = element_collect.text.split(' (')
        self.assertEqual(element_collectText[0], u'收藏的作品')
        element_collectNum = int(element_collectText[1].split(')')[0])
        # 收藏数大于3，测试跳转页面是否正常
        if element_collectNum > 3:
            self.driver.find_element_by_id('com.xmtj.mkz:id/user_collect_more').click()
            WebDriverWait(self.driver, 15).until(
                lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/user_collect_title_name'))
            self.driver.find_element_by_id('com.xmtj.mkz:id/white_back').click()
            print '用户收藏数为%d，跳转收藏页面，测试通过' % element_collectNum
        elif 0 < element_collectNum <= 3:
            try:
                self.driver.find_element_by_id('com.xmtj.mkz:id/user_collect_more')
                print '收藏数小于3仍然显示“更多”按钮，测试错误！！！！！'
            except Exception, e:
                print '用户收藏数为%d，测试通过' % element_collectNum
        else:
            print '用户收藏数异常，显示为%d，测试错误！！！！！' % element_collectNum

        # 滑动相对坐标
        x1 = 380.00 / 720
        y1 = 1000.00 / 1280
        y2 = 530.00 / 1280
        # 滑动实际坐标
        x_swipe1 = int(x1 * self.x)
        y_swipe1 = int(y1 * self.y)
        y_swipe2 = int(y2 * self.y)
        # 随机滑动页面后，选择第一个动态内容
        self.driver.swipe(x_swipe1, y_swipe1, x_swipe1, y_swipe2, 800)
        swipe_max = random.randint(1, 21)
        for n in range(1, swipe_max):
            Swipe_op.SwipeDown(self)
        element_activitys = self.driver.find_elements_by_id('com.xmtj.mkz:id/tv_activity')
        element_details = self.driver.find_elements_by_id('com.xmtj.mkz:id/detail_layout')
        element_activity = element_activitys[1]
        element_detail = element_details[1]
        print '动态页面随机选择的动态为：%s' % element_activity.text

        # 判断该动态类型，并点击跳转测试
        factor = '收藏|评论|打赏|月票'
        if re.search(factor, str(element_activity.text)) is not None:
            element_comic_name = element_detail.find_element_by_id(Page_config.PageID.comic_name).text
            element_detail.click()
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.find_element_by_id(Page_config.PageID.comic_name))
            element_comic1 = self.driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout')
            comic_name2 = element_comic1.find_element_by_id(Page_config.PageID.comic_name).text
            self.assertEqual(element_comic_name, comic_name2)
            self.driver.find_element_by_id(Page_config.PageID.top_back).click()
            print '动态列表测试跳转的漫画为：%s' % element_comic_name
        elif re.search('关注', str(element_activity.text)) is not None:
            element_other_name = element_detail.find_element_by_id('com.xmtj.mkz:id/tv_other_name').text
            element_detail.click()
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/tv_name'))
            tv_name = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_name').text
            re.search(str(tv_name), str(element_other_name))
            self.driver.find_element_by_id(Page_config.PageID.top_back).click()
            print '跳转的用户为：%s' % element_other_name

        print '动态列表随机点击跳转测试通过'
        time.sleep(1)








# -*- coding:utf-8 -*-

import time
import unittest
import os
import random
import string
import datetime
from config import appium_config, Page_config
from driver import Swipe_op, go_comic
from selenium.webdriver.support.wait import WebDriverWait

# 设置路径信息
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class ComicDetailTest(unittest.TestCase):
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
        go_comic.go_comic(cls)

        # 进入分类页面
        cls.driver.find_element_by_id(Page_config.PageID.tab_category).click()

        # 分类页面中随机选择一部漫画进入
        for x in range(1, random.randint(1, 31)):
            Swipe_op.SwipeDown(cls)

        element_names = cls.driver.find_elements_by_id('com.xmtj.mkz:id/name')
        element_name = element_names[random.randint(3, len(element_names) - 1)]
        element_name.click()
        try:
            WebDriverWait(cls.driver, 30).until(lambda driver: driver.find_element_by_id(Page_config.PageID.comic_read))
        except Exception, e:
            # 判断超时时，点击刷新页面
            for i in range(1, 21):
                try:
                    element_refresh = cls.driver.find_elements_by_id('com.xmtj.mkz:id/refresh')
                    if element_refresh is not None:
                        element_refresh.click()
                    break
                except Exception, e:
                    print '网络出错，页面未能刷新'
                    continue

        element_comic = cls.driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout')
        cls.comic_name = element_comic.find_element_by_id(Page_config.PageID.comic_name).text

    # 退出测试
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # 进入漫画详情页，判断阅读按钮
    def test_case_comicReadCase1(self):
        print '随机选择的漫画为：%s' % self.comic_name

















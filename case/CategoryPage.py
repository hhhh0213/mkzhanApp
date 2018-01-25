# -*- coding:utf-8 -*-

import time
import unittest
import os
import random
from config import appium_config, Page_config
from driver.GetImg import Appium_Extend
from driver import Swipe_op, go_comic
from selenium.webdriver.support.wait import WebDriverWait

# 设置路径信息
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class CategoryTest(unittest.TestCase):
    global driver

    # 初始化环境
    @classmethod
    def setUpClass(cls):
        # 更改Appium启动参数
        appium_config.desired_caps['automationName'] = 'Appium'
        # 启动Appium
        appium_config.AppiumStart(cls)
        cls.extend = Appium_Extend(cls.driver)

        # 获取手机屏幕分辨率
        cls.x = cls.driver.get_window_size()['width']
        cls.y = cls.driver.get_window_size()['height']

        time.sleep(5)

        # 判断是否存在收藏提醒
        go_comic.go_comic(cls)

        # 进入分类页面
        cls.driver.find_element_by_id('com.xmtj.mkz:id/tab_category').click()

    # 退出测试
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_case_categoryTest(self):
        element = self.driver.find_element_by_id('com.xmtj.mkz:id/label_layout')
        elements_cat = element.find_elements_by_class_name('android.widget.TextView')

        # 分类滑动相对坐标
        x1 = 500.00 / 720
        x2 = 300.00 / 720
        y1 = 190.00 / 1280
        # 分类滑动实际坐标
        x_swipe1 = int(x1 * self.x)
        x_swipe2 = int(x2 * self.x)
        y_swipe1 = int(y1 * self.y)
        # 随机滑动分类栏并随机点击
        for swipe in range(0, random.randint(0, 9)):
            self.driver.swipe(x_swipe1, y_swipe1, x_swipe2, y_swipe1, 800)
        cat_num = random.randint(0, len(elements_cat) - 1)
        elements_cat[cat_num].click()
        print '点击的漫画分类为：%s' % elements_cat[cat_num].text
        time.sleep(1)

        # 随机点击状态分类
        list1 = ['com.xmtj.mkz:id/status_all', 'com.xmtj.mkz:id/status_serialize', 'com.xmtj.mkz:id/status_end']
        status_num1 = random.randint(0, 2)
        element_status1 = self.driver.find_element_by_id(list1[status_num1])
        element_status1.click()
        print '点击的漫画状态分类为：%s' % element_status1.text
        time.sleep(1)

        # 随机点击售价分类
        list2 = ['com.xmtj.mkz:id/price_all', 'com.xmtj.mkz:id/price_free', 'com.xmtj.mkz:id/price_fee', 'com.xmtj.mkz:id/price_vip']
        status_num2 = random.randint(0, 3)
        element_status2 = self.driver.find_element_by_id(list2[status_num2])
        element_status2.click()
        print '点击的漫画售价分类为：%s' % element_status2.text

        try:
            WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/chapter'))
            # 随机下滑页面
            swipe_num = random.randint(0, 11)
            for x in range(0, swipe_num):
                Swipe_op.SwipeDown(self)

            # 随机选择分类列表中的漫画，并判断是否连载/完结
            elements_comic = self.driver.find_elements_by_id('com.xmtj.mkz:id/chapter')
            element_comic = elements_comic[random.randint(0, len(elements_comic) - 1)]
            if element_comic.text.split('至')[0] == '更新':
                print '漫画处于连载状态'
            elif element_comic.text == '完结':
                print '漫画处于完结状态'
            element_comic.click()
            WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout'))
            element_comic = self.driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout')
            comic_name = element_comic.find_element_by_id(Page_config.PageID.comic_name).text

            print '分类测试点击的漫画为：%s' % comic_name
            self.driver.find_element_by_id(Page_config.PageID.top_back).click()

        except Exception, e:
            self.driver.find_element_by_id('com.xmtj.mkz:id/empty_text')
            print '该分类下无漫画数据'




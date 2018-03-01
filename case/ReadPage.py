# -*- coding:utf-8 -*-

import time
import unittest
import os
import random
import string

from config import appium_config, Page_config
from driver import Swipe_op, go_comic
from selenium.webdriver.support.wait import WebDriverWait

# 设置路径信息
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class ComicReadTest(unittest.TestCase):
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

    # 退出测试
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # 判断漫画章节是否需要购买
    def test_case_comicReadCase1(self):
        # 分类页面中随机选择免费/付费选项
        list1 = ['com.xmtj.mkz:id/price_free', 'com.xmtj.mkz:id/price_fee', 'com.xmtj.mkz:id/price_vip']
        status_num = random.randint(0, 2)
        element_status = self.driver.find_element_by_id(list1[status_num])
        element_status.click()
        print '随机选择的分类为：%s' % element_status.text

        # 分类页面中随机选择一部漫画进入
        for x in range(1, random.randint(1, 31)):
            Swipe_op.SwipeDown(self)

        element_names = self.driver.find_elements_by_id('com.xmtj.mkz:id/name')
        element_name = element_names[random.randint(3, len(element_names) - 1)]
        element_name.click()
        try:
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id(Page_config.PageID.comic_read))
        except Exception, e:
            # 判断超时时，点击刷新页面
            for i in range(1, 21):
                try:
                    element_refresh = self.driver.find_elements_by_id('com.xmtj.mkz:id/refresh')
                    if element_refresh is not None:
                        element_refresh.click()
                    break
                except Exception, e:
                    print '网络出错，页面未能刷新'
                    continue

        element_comic = self.driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout')
        comic_name = element_comic.find_element_by_id(Page_config.PageID.comic_name).text
        print '随机选择的漫画为：%s' % comic_name

        # 进入阅读页
        self.driver.find_element_by_id(Page_config.PageID.comic_read).click()
        time.sleep(3)

        try:
            # 判断元宝是否能够购买章节
            comic_price = self.driver.find_element_by_id('com.xmtj.mkz:id/price').text
            my_money = self.driver.find_element_by_id('com.xmtj.mkz:id/normal_balance').text
            if string.atoi(my_money) - string.atoi(comic_price) >= 0:
                normal_buy = self.driver.find_element_by_id('com.xmtj.mkz:id/normal_buy').text
                self.assertEqual(normal_buy, u'立即购买，开启阅读')
                print '该章节收费：%s；用户元宝数为：%s，可以购买该章节' % (comic_price, my_money)
                # self.driver.find_element_by_id('com.xmtj.mkz:id/normal_buy').click()
            else:
                other_buy = self.driver.find_element_by_id('com.xmtj.mkz:id/vip_buy').text
                self.assertEqual(other_buy, u'元宝余额不足，点击充值')
                print '该章节收费：%s；用户元宝数为：%s，不能购买该章节' % (comic_price, my_money)
                # self.driver.find_element_by_id('com.xmtj.mkz:id/vip_buy').click()

            # 判断VIP状态与阅读页按钮显示是否对应
            normal_layout = self.driver.find_element_by_id('com.xmtj.mkz:id/normal_layout')
            layout_text = normal_layout.find_elements_by_class_name('android.widget.TextView')
            if layout_text[1].text == u'您不是VIP会员':
                normal_buy_vip = self.driver.find_element_by_id('com.xmtj.mkz:id/normal_buy_vip').text
                if element_status.text == u'付费':
                    self.assertEqual(normal_buy_vip, u'开通VIP，购买章节8折优惠')
                if element_status.text == u'VIP':
                    self.assertEqual(normal_buy_vip, u'开通VIP，开启免费阅读')
                print '用户不是VIP，开通按钮显示正常'
                # self.driver.find_element_by_id('com.xmtj.mkz:id/normal_buy_vip').click()
            else:
                try:
                    self.driver.find_element_by_id('com.xmtj.mkz:id/normal_buy_vip')
                    print '用户已是VIP，但仍显示开通VIP按钮'
                except Exception, e:
                    print '用户已是VIP，不显示开通VIP按钮'
            return True
        except Exception, e:
            print '该章节为免费/已付费章节，可正常阅读'
            return False

    # 章节免费/已付费，可以正常阅读；否则跳过阅读页测试用例
    @unittest.skipIf(test_case_comicReadCase1 is True, 'ererer')
    def test_case_comicReadCase2(self):
        # 获取屏幕中心位置
        x1 = 360.00 / 720
        y1 = 600.00 / 1280
        x_click = int(x1 * self.x)
        y_click = int(y1 * self.y)
        # 获取底部信息栏各元素，进行测试
        try:
            chapter_text = self.driver.find_element_by_id('com.xmtj.mkz:id/chapter').text
            # 点击屏幕中心弹出功能栏
            self.driver.tap([(x_click, y_click)])
            WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/title'))
            title_text = self.driver.find_element_by_id('com.xmtj.mkz:id/title').text
            print '当前阅读的漫画章节为：%s；底部信息栏显示的信息为：%s' % (title_text, chapter_text)
        except Exception, e:
            print e

        # 点击横屏，测试是否正常
        tab_screen = self.driver.find_element_by_id('com.xmtj.mkz:id/tab_screen')
        self.assertEqual(tab_screen.text, u'横屏')
        tab_screen.click()
        # 点击屏幕隐藏切换提示
        x2 = 600.00 / 720
        y2 = 250.00 / 1280
        x_click1 = int(x2 * self.x)
        y_click1 = int(y2 * self.y)
        self.driver.tap([(x_click1, y_click1)])
        WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/chapter'))
        # 随机下滑页面
        swipe_num = random.randint(10, 60)
        for x in range(1, swipe_num + 1):
            Swipe_op.SwipeDown(self)
        try:
            chapter_text1 = self.driver.find_element_by_id('com.xmtj.mkz:id/chapter').text
            chapter_position1 = self.driver.find_element_by_id('com.xmtj.mkz:id/chapter_position').text
            self.driver.tap([(x_click1, y_click1)])
            self.assertEqual(tab_screen.text, u'竖屏')
            title_text1 = self.driver.find_element_by_id('com.xmtj.mkz:id/title').text
            print '随机向下滑动阅读页后，当前漫画章节进度为：%s；底部信息栏显示的章节信息为：%s %s' % (title_text1, chapter_text1, chapter_position1)
        except Exception, e:
            print e
        tab_screen.click()
        time.sleep(2)
        self.driver.tap([(x_click1, y_click1)])
        time.sleep(2)
        self.driver.tap([(x_click, y_click)])
        print '测试漫画阅读页切换横竖屏功能正常'
        time.sleep(4)

        # 滑动底部进度条提示
        x2_1 = 170.00 / 720
        x2_2 = 500.00 / 720
        y2 = 1115.00 / 1280
        x_swipe1 = int(x2_1 * self.x)
        x_swipe2 = int(x2_2 * self.x)
        y_swipe1 = int(y2 * self.y)
        self.driver.swipe(x_swipe1, y_swipe1, x_swipe2, y_swipe1, 1200)
        title_text2 = self.driver.find_element_by_id('com.xmtj.mkz:id/title').text
        self.driver.tap([(x_click, y_click)])
        chapter_text2 = self.driver.find_element_by_id('com.xmtj.mkz:id/chapter').text
        chapter_position2 = self.driver.find_element_by_id('com.xmtj.mkz:id/chapter_position').text
        print '随机滑动底部进度条，当前漫画章节进度为：%s；底部信息栏显示的章节信息为：%s %s' % (title_text2, chapter_text2, chapter_position2)
        time.sleep(2)

        # 测试目录按钮
        self.driver.find_element_by_id('com.xmtj.mkz:id/tab_chapter').click()
        WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/sort'))
        element_sort = self.driver.find_element_by_id('com.xmtj.mkz:id/sort')
        self.assertEqual(element_sort.text, u'倒序')
        element_sort.click()
        time.sleep(3)
        self.assertEqual(element_sort.text, u'正序')
        self.driver.tap([(x_click, y_click)])

        # 阅读页功能按钮
        self.driver.tap([(x_click, y_click)])
        self.driver.find_element_by_id('com.xmtj.mkz:id/menu_more').click()
        WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/menu_list'))
        self.driver.find_element_by_id('com.xmtj.mkz:id/menu_feedback').click()
        WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/tv_feedback'))
        self.driver.find_element_by_id(Page_config.PageID.backButtonID).click()















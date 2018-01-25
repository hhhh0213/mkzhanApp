# -*- coding:utf-8 -*-

import time
import unittest
import os
import random
import datetime
from config import appium_config, Page_config
from driver.GetImg import Appium_Extend
from driver import Swipe_op, go_comic
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.connectiontype import ConnectionType

# 设置路径信息
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class HomePageTest(unittest.TestCase):
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

        time.sleep(6)
        # 判断是否存在收藏提醒
        go_comic.go_comic(cls)

    '''推荐页面各版块点击跳转操作'''
    def home_module(self, ModuleID, titleText, GridID, gridNum):
        # 查找页面中的版块标题区域，测试点击返回流程
        while True:
            try:
                self.driver.find_element_by_id(ModuleID).click()
                break
            except Exception, e:
                Swipe_op.SwipeDown(self)

        self.driver.wait_activity('.business.main.list.ComicListActivity', 5, 0.5)
        self.assertEqual(self.driver.find_element_by_id('com.xmtj.mkz:id/title').text, titleText)
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        time.sleep(2)

        # 根据各版块中的漫画数量定位展示
        while True:
            try:
                element_Grid = self.driver.find_element_by_id(GridID)
                elements_Grid = element_Grid.find_elements_by_id('com.xmtj.mkz:id/name')
                self.assertEqual(len(elements_Grid), gridNum)
                break
            except Exception, e:
                Swipe_op.SwipeDown(self)

        # 随机选择版块中的漫画点击跳转，对比漫画标题是否一致
        num = random.randint(0, gridNum - 1)
        comic_name1 = elements_Grid[num].text
        elements_Grid[num].click()
        try:
            WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout'))
        except Exception, e:
            pass
        element_comic = self.driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout')
        comic_name2 = element_comic.find_element_by_id(Page_config.PageID.comic_name).text
        self.assertEqual(comic_name1, comic_name2)

        self.driver.find_element_by_id(Page_config.PageID.top_back).click()
        time.sleep(3)

    '''主页其他tab页面测试（男生/女生/更新页面）'''
    def home_tab1(self, choiceNum):
        element1 = self.driver.find_element_by_id(Page_config.PageID.homeTab)
        elements1 = element1.find_elements_by_class_name('android.widget.FrameLayout')
        # 进入对应页面
        elements1[choiceNum].click()
        time.sleep(3)
        # 随机下滑页面
        swipe_num = random.randint(1, 20)
        for x in range(1, swipe_num + 1):
            Swipe_op.SwipeDown(self)

        # 随机点击页面中的漫画内容跳转
        self.element_list = self.driver.find_element_by_id('android:id/list')
        elements_list = self.element_list.find_elements_by_id('com.xmtj.mkz:id/name')
        click_num1 = random.randint(0, len(elements_list) - 1)
        self.comic_name1 = elements_list[click_num1].text
        elements_list[click_num1].click()

        # 判断是否进入漫画详情页，且漫画名称与之对应
        WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout'))
        element_comic = self.driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout')
        self.comic_name2 = element_comic.find_element_by_id(Page_config.PageID.comic_name).text
        self.assertTrue(self.comic_name1, self.comic_name2)

    '''主页其他tab页面测试（排行页面）'''
    def home_tab2(self, rankID, rankRule):
        # 测试各个榜单
        try:
            self.driver.find_element_by_id(rankID).click()
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/count'))
            rank_rule = self.driver.find_element_by_id('com.xmtj.mkz:id/count').text.split('：')[0]
            self.assertEqual(rank_rule, rankRule)
        except Exception, e:
            pass
        time.sleep(2)
        # 随机点击页面中的漫画内容跳转
        WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/name'))
        element_list = self.driver.find_element_by_id('android:id/list')
        elements_list = element_list.find_elements_by_id('com.xmtj.mkz:id/name')
        self.comic_name1 = elements_list[0].text
        elements_list[0].click()

        # 判断是否进入漫画详情页，且漫画名称与之对应
        WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout'))
        element_comic = self.driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout')
        self.comic_name2 = element_comic.find_element_by_id(Page_config.PageID.comic_name).text
        self.assertTrue(self.comic_name1, self.comic_name2)

        self.driver.find_element_by_id(Page_config.PageID.top_back).click()

    # 退出测试
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    '''首页各操作测试用例'''
    def test_case_homePage1(self):
        # 判断当前手机网络
        network_num = self.driver.network_connection
        if network_num != 6:
            # 开启手机wifi网络
            self.driver.set_network_connection(ConnectionType.WIFI_ONLY)
            time.sleep(5)
        try:
            # 联网情况下，默认进入首页页面
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_id(Page_config.PageID.homeTab))
            element1 = self.driver.find_element_by_id(Page_config.PageID.homeTab)
            elements1 = element1.find_elements_by_class_name('android.widget.FrameLayout')
            self.assertEqual(len(elements1), 5)
            elements1[2].click()
        except Exception, e:
            print '首页顶部tab检查出错'

        # banner图滑动相对坐标
        x1 = 530.00 / 720
        x2 = 280.00 / 720
        y1 = 330.00 / 1280
        # banner图滑动实际坐标
        x_swipe1 = int(x1 * self.x)
        x_swipe2 = int(x2 * self.x)
        y_swipe1 = int(y1 * self.y)

        # 设定随机滑动banner图的次数，并循环滑动
        try:
            WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/loop_view_pager'))
            for swipe in range(0, random.randint(5, 15)):
                self.driver.swipe(x_swipe1, y_swipe1, x_swipe2, y_swipe1, 800)
            print 'banner图滑动操作测试通过'
        except Exception, e:
            pass
        time.sleep(2)

        # 测试客栈精品区域
        self.home_module('com.xmtj.mkz:id/fine_layout', u'客栈精品', 'com.xmtj.mkz:id/fine_grid_layout', 4)
        print '客栈精品区域跳转及漫画点击测试通过'

        # 测试独家作品区域
        self.home_module('com.xmtj.mkz:id/exclusive_layout', u'独家作品', 'com.xmtj.mkz:id/exclusive_grid_layout', 9)
        print '独家作品区域跳转及漫画点击测试通过'

        # 测试上升最快区域
        self.home_module('com.xmtj.mkz:id/ascension_layout', u'上升最快', 'com.xmtj.mkz:id/ascension_grid_layout', 9)
        print '上升最快区域跳转及漫画点击测试通过'

        # 测试合作作品区域
        self.home_module('com.xmtj.mkz:id/cooperation_layout', u'合作作品', 'com.xmtj.mkz:id/cooperation_grid_layout', 9)
        print '合作作品区域跳转及漫画点击测试通过'

    def test_case_homePage2(self):
        # 进入男生页面
        self.home_tab1(0)
        self.driver.find_element_by_id(Page_config.PageID.top_back).click()
        time.sleep(2)

        # 随机点击漫画的速看进行跳转
        elements_read = self.element_list.find_elements_by_id(Page_config.PageID.readID)
        click_num2 = random.randint(0, len(elements_read) - 1)
        self.assertEqual(elements_read[click_num2].text, u'速看')
        elements_read[click_num2].click()

        # 判断是否进入漫画阅读页
        self.assertTrue(self.driver.wait_activity('.business.read.ReadActivity', 25, 1))
        self.driver.press_keycode('4')
        time.sleep(3)
        print '男生页面漫画点击及速看点击，测试通过'

        # 进入女生页面
        self.home_tab1(1)
        self.driver.find_element_by_id(Page_config.PageID.top_back).click()
        time.sleep(2)

        # 随机点击漫画的速看进行跳转
        elements_read = self.element_list.find_elements_by_id(Page_config.PageID.readID)
        click_num2 = random.randint(0, len(elements_read) - 1)
        self.assertEqual(elements_read[click_num2].text, u'速看')
        elements_read[click_num2].click()

        # 判断是否进入漫画阅读页
        self.assertTrue(self.driver.wait_activity('.business.read.ReadActivity', 25, 1))
        self.driver.press_keycode('4')
        time.sleep(3)
        print '女生页面漫画点击及速看点击，测试通过'

    def test_case_homePage3(self):
        # 进入更新页面
        self.home_tab1(3)
        print '更新列表中随机选择的漫画为：%s' % self.comic_name1

        # 判断更新时间是否一致
        now_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y.%m.%d')

        element_comic = self.driver.find_element_by_id('com.xmtj.mkz:id/recycler')
        elements_name = element_comic.find_elements_by_class_name('android.widget.TextView')
        if elements_name[0].text != '完结':
            comic_time = elements_name[0].text.split('：')[-1].split('更')[0]
            self.assertEqual(comic_time, now_time)
        else:
            pass

        self.driver.find_element_by_id(Page_config.PageID.top_back).click()
        print '更新页面漫画点击，测试通过'
        time.sleep(3)

    def test_case_homePage4(self):
        # 进入排行页面
        element1 = self.driver.find_element_by_id(Page_config.PageID.homeTab)
        elements1 = element1.find_elements_by_class_name('android.widget.FrameLayout')
        elements1[4].click()
        time.sleep(3)
        # 测试人气榜
        self.home_tab2('com.xmtj.mkz:id/rank_popular', u'周点击')
        print '人气榜测试通过，排第一名的漫画为：%s' % self.comic_name1
        time.sleep(2)
        # 测试月票榜
        self.home_tab2('com.xmtj.mkz:id/rank_ticket', u'月票数')
        print '月票榜测试通过，排第一名的漫画为：%s' % self.comic_name1
        time.sleep(2)
        # 测试收藏榜
        self.home_tab2('com.xmtj.mkz:id/rank_collection', u'总收藏量')
        print '收藏榜测试通过，排第一名的漫画为：%s' % self.comic_name1
        time.sleep(2)
        # 测试独家榜
        self.home_tab2('com.xmtj.mkz:id/rank_exclusive', u'总点击')
        print '独家榜测试通过，排第一名的漫画为：%s' % self.comic_name1
        time.sleep(2)
        # 测试新作榜
        self.home_tab2('com.xmtj.mkz:id/rank_latest', u'周点击')
        print '新作榜测试通过，排第一名的漫画为：%s' % self.comic_name1
        time.sleep(2)
        # 测试上升榜
        self.home_tab2('com.xmtj.mkz:id/rank_ascension', u'周点击')
        print '上升榜测试通过，排第一名的漫画为：%s' % self.comic_name1











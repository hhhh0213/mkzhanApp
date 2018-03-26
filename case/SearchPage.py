# -*- coding:utf-8 -*-

import string
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


class SearchTest(unittest.TestCase):
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

        # 进入搜索页面
        cls.driver.find_element_by_id('com.xmtj.mkz:id/search').click()

    # 退出测试
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_case_searchCase1(self):
        # 随机选择热门搜索词
        element_hotSearchID = self.driver.find_element_by_id('com.xmtj.mkz:id/hot_key_layout')
        elements_hotKey = element_hotSearchID.find_elements_by_class_name('android.widget.TextView')
        element_hotKey = elements_hotKey[random.randint(0, len(elements_hotKey) - 1)]
        element_hotKey_name = element_hotKey.text
        element_hotKey.click()

        try:
            WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout'))
        except Exception, e:
            pass
        element_comic = self.driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout')
        comic_name = element_comic.find_element_by_id(Page_config.PageID.comic_name).text
        self.assertEqual(element_hotKey_name, comic_name)

        self.driver.find_element_by_id(Page_config.PageID.top_back).click()
        print '热门搜索测试通过\n随机选择的热门搜索漫画为：%s' % element_hotKey_name
        time.sleep(2)

    def test_case_searchCase2(self):
        # 随机从实时搜索显示中，点击一部漫画
        self.driver.find_element_by_id('com.xmtj.mkz:id/edit').send_keys(u'斗')
        WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id(Page_config.PageID.comic_name))
        element_suggestID = self.driver.find_element_by_id('com.xmtj.mkz:id/suggest_list')
        elements_suggest = element_suggestID.find_elements_by_id(Page_config.PageID.comic_name)
        element_suggest = elements_suggest[random.randint(0, len(elements_suggest) - 1)]
        element_suggest_name = element_suggest.text
        element_suggest.click()

        try:
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout'))
        except Exception, e:
            pass
        element_comic = self.driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout')
        comic_name = element_comic.find_element_by_id(Page_config.PageID.comic_name).text
        self.assertEqual(element_suggest_name, comic_name)

        self.driver.find_element_by_id(Page_config.PageID.top_back).click()
        print '实时搜索测试通过\n随机选择的实时搜索结果漫画为：%s' % element_suggest_name
        time.sleep(2)

    def test_case_searchCase3(self):
        # 随机从搜索结果中点击一部漫画
        self.driver.find_element_by_id('com.xmtj.mkz:id/cancel_sure').click()

        WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id('android:id/list'))
        swipe_num = random.randint(1, 10)
        for x in range(1, swipe_num + 1):
            Swipe_op.SwipeDown(self)
        # 随机点击页面中的漫画内容跳转
        element_list = self.driver.find_element_by_id('android:id/list')
        elements_list = element_list.find_elements_by_id(Page_config.PageID.comic_name)
        click_num1 = random.randint(0, len(elements_list) - 1)
        comic_name1 = elements_list[click_num1].text
        elements_list[click_num1].click()

        # 判断是否进入漫画详情页，且漫画名称与之对应
        WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout'))
        element_comic = self.driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout')
        comic_name2 = element_comic.find_element_by_id(Page_config.PageID.comic_name).text
        self.assertTrue(comic_name1, comic_name2)
        self.driver.find_element_by_id(Page_config.PageID.top_back).click()

        print '存在搜索结果的测试通过\n搜索结果中点击的漫画为：%s' % comic_name1
        time.sleep(2)

    def test_case_searchCase4(self):
        self.driver.find_element_by_id('com.xmtj.mkz:id/edit').clear()
        # 随机输入无搜索结果的关键词
        tmp = list(string.lowercase)
        keyTest = ''.join(random.sample(tmp, random.randint(5, 10)))
        self.driver.find_element_by_id('com.xmtj.mkz:id/edit').send_keys('%s' % keyTest)
        self.driver.find_element_by_id('com.xmtj.mkz:id/cancel_sure').click()
        time.sleep(2)
        element_search = self.driver.find_element_by_id('android:id/list')
        search_result = element_search.find_elements_by_class_name('android.widget.TextView')[0]
        if search_result.text == u'主人,搜索不到目标':
            print '搜索 %s 关键词无结果，测试通过' % keyTest
        else:
            print '搜索无结果出错'
        '''
        # 搜索结果页面输入框内的删除图标相对坐标
        x1 = 560.00 / 720
        y1 = 90.00 / 1280
        # 测试实际坐标
        x_click1 = int(x1 * self.x)
        y_click1 = int(y1 * self.y)
        self.driver.tap([(x_click1, y_click1)])
        time.sleep(3)
        '''
        self.driver.press_keycode('4')
        time.sleep(2)

    def test_case_searchCase5(self):
        self.driver.find_element_by_id('com.xmtj.mkz:id/search').click()
        element_history = self.driver.find_element_by_id('com.xmtj.mkz:id/history_layout')
        element_title = element_history.find_elements_by_id('com.xmtj.mkz:id/title')
        element_items = element_history.find_elements_by_id('com.xmtj.mkz:id/item_clear')
        title1 = element_title[0].text
        element_items[0].click()
        title2 = element_title[0].text
        self.assertNotEqual(title1, title2)
        time.sleep(2)
        self.driver.find_element_by_id('com.xmtj.mkz:id/clear_history').click()
        self.driver.find_element_by_id('com.xmtj.mkz:id/sure').click()
        try:
            self.driver.find_element_by_id('com.xmtj.mkz:id/history_title_layout')
            print '清除历史出错'
        except Exception, e:
            print '清除历史功能测试通过'

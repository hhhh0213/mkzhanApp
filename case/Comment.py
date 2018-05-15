# -*- coding:utf-8 -*-

import time
import unittest
import os
import random
from config import appium_config, Page_config
from driver import Swipe_op, go_comic, GetToast
from selenium.webdriver.support.wait import WebDriverWait

# 设置路径信息
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class ComicCommentTest(unittest.TestCase):
    global driver

    # 初始化环境
    @classmethod
    def setUpClass(cls):
        # 更改Appium启动参数
        appium_config.desired_caps['automationName'] = 'Uiautomator2'
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

        # 进入分类页面
        cls.driver.find_element_by_id(Page_config.PageID.tab_category).click()

        # 分类页面中随机选择一部漫画进入
        for x in range(1, random.randint(3, 31)):
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

    # 测试漫画详情页评论
    def test_case_CommentCase1(self):
        print '随机选择的漫画为：%s' % self.comic_name
        time.sleep(3)

        comment_num = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_comment_count').text
        comment_num_str = comment_num.encode("utf-8")
        comment_num1 = int("".join(filter(str.isdigit, comment_num_str)))
        self.driver.find_element_by_id('com.xmtj.mkz:id/comment_layout').click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id(Page_config.PageID.titleID))
        comment_title = self.driver.find_element_by_id(Page_config.PageID.titleID).text
        element_comment_str = comment_title.encode("utf-8")
        element_comment_num = int("".join(filter(str.isdigit, element_comment_str)))
        # 判断评论数量大于99时，icon数字的显示是否正确
        if element_comment_num > 99:
            self.assertEqual(comment_num, u'99+')
        elif element_comment_num <= 99:
            self.assertEqual(element_comment_num, comment_num1)
        print '该漫画的评论数在漫画详情页显示为：%s，实际评论总数为：%d' % (comment_num, element_comment_num)
        time.sleep(2)

        # 进入发表评论页面
        self.driver.find_element_by_xpath('//android.widget.ImageView[contains(@index,1)]').click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/btn_add_comment'))

        # 评论为空，发布按钮不能点击
        add_comment = self.driver.find_element_by_id('com.xmtj.mkz:id/btn_add_comment')
        self.assertEqual(add_comment.get_attribute('clickable'), u'false')
        print '评论为空，发布按钮不能点击，测试通过'
        # 评论字数不足
        self.driver.find_element_by_id('com.xmtj.mkz:id/edit').send_keys(u'不错不')
        add_comment.click()
        GetToast.find_toast(u'评论内容必须在4-200个字符之间', 30, 0.1, self.driver)
        print '评论字数不符合规则，不能发布，测试通过'
        # 评论成功
        self.driver.find_element_by_id('com.xmtj.mkz:id/edit').send_keys(u'不错不错，加油大大！')
        add_comment.click()
        GetToast.find_toast(u'发布评论成功', 30, 0.1, self.driver)
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id(Page_config.PageID.titleID))
        time.sleep(2)
        comment_content_text1 = self.driver.find_element_by_id('com.xmtj.mkz:id/comment_content').text
        self.assertEqual(comment_content_text1, u'不错不错，加油大大！')
        print '评论发布成功，测试通过'
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/comment_content'))
        self.driver.find_element_by_id('com.xmtj.mkz:id/comment_content').click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/send'))
        # 回复为空不能点击发布
        reply_comment = self.driver.find_element_by_id('com.xmtj.mkz:id/send')
        self.assertEqual(reply_comment.get_attribute('enabled'), u'false')
        print '评论回复为空，发布按钮不能点击，测试通过'
        # 回复内容字数不符合规则
        self.driver.find_element_by_id('com.xmtj.mkz:id/edit').send_keys(u'666')
        reply_comment.click()
        GetToast.find_toast(u'评论内容必须在4-200个字符之间', 30, 0.1, self.driver)
        print '评论回复字数不符合规则，不能发布，测试通过'
        # 评论回复成功
        self.driver.find_element_by_id('com.xmtj.mkz:id/edit').send_keys(u'6666')
        reply_comment.click()
        GetToast.find_toast(u'回复评论成功', 30, 0.1, self.driver)
        print '评论回复发布成功，测试通过'
        for n in range(0, 2):
            self.driver.find_element_by_accessibility_id('转到上一层级').click()
            time.sleep(3)

        # 刷新漫画详情页
        x1 = 520.00 / 1080
        y1 = 300.00 / 1920
        y2 = 850.00 / 1920
        # 实际坐标
        x_swipe1 = int(x1 * self.x)
        y_swipe1 = int(y1 * self.y)
        y_swipe2 = int(y2 * self.y)
        self.driver.swipe(x_swipe1, y_swipe1, x_swipe1, y_swipe2, 3000)
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/comment_layout'))

        # 判断评论本地是否缓存成功
        self.driver.find_element_by_id('com.xmtj.mkz:id/comment_layout').click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/comment_content'))
        comment_list1 = self.driver.find_elements_by_id('com.xmtj.mkz:id/comment_content')
        comment_content = comment_list1[0].text
        self.assertEqual(comment_content, u'不错不错，加油大大！')
        print '评论本地缓存成功'

        # 进入评论详情页面
        comment_list1[0].click()
        time.sleep(3)
        comment_list2 = self.driver.find_elements_by_id('com.xmtj.mkz:id/comment_content')
        reply_content = comment_list2[1].text
        self.assertEqual(reply_content, u'6666')
        print '评论回复本地缓存成功'
















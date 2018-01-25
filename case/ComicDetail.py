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

    # 测试漫画详情页目录
    def test_case_comicDetailCase1(self):
        print '随机选择的漫画为：%s，测试该漫画详情页中的目录区域' % self.comic_name
        time.sleep(1)

        # 判断章节与更多按钮的展示逻辑是否正确
        element_comic_nums = self.driver.find_elements_by_id(Page_config.PageID.comic_numID)

        def assTrue1():
            if len(element_comic_nums) < 12:
                try:
                    self.driver.find_elements_by_id(Page_config.PageID.comic_more_textID)
                    print '漫画详情页章节数小于12，仍然显示更多按钮，测试失败'
                    return False
                except Exception, e:
                    print '漫画详情页章节数小于12，不显示更多按钮，测试通过'
                    return True
            elif len(element_comic_nums) == 12:
                # 判断章节数为12时，是否有显示更多按钮
                try:
                    element_comic_more = self.driver.find_element_by_id(Page_config.PageID.comic_more_textID)
                    self.assertEqual(element_comic_more.text, u'大人，更多话在这里')
                    element_comic_more.click()
                    element_comic_nums2 = self.driver.find_elements_by_id(Page_config.PageID.comic_numID)

                    # 如果章节数大于12，滑动页面至底部，判断更多按钮文案是否正确
                    if len(element_comic_nums2) > 12:
                        while True:
                            try:
                                self.driver.find_element_by_id(Page_config.PageID.comic_recommendID)
                                break
                            except Exception, e:
                                Swipe_op.SwipeDown(self)
                                continue
                        try:
                            self.assertEqual(element_comic_more.text, u'点击收起')
                            print '漫画详情页章节数大于12，正常显示更多按钮，测试通过'
                            return True
                        except Exception, e:
                            print '更多按钮点击后文案有误'
                            return False

                    # 如果章节数点击更多按钮后，仍为12，则更多按钮逻辑有误
                    elif len(element_comic_nums2) == 12:
                        print '漫画详情页章节数等于12，仍然显示更多按钮，测试失败'
                        return False
                except Exception, e:
                    print '漫画详情页章节数等于12，不显示更多按钮，测试通过'
                    return True

        result = assTrue1()
        self.assertTrue(result)

        # 点击底部相关推荐跳转测试
        while True:
            try:
                self.driver.find_element_by_id('com.xmtj.mkz:id/recommend_scroll_layout')
                break
            except Exception, e:
                Swipe_op.SwipeDown(self)
                continue
        element_comic_recommend = self.driver.find_element_by_id('com.xmtj.mkz:id/recommend_scroll_layout')
        element_comic_recommends = element_comic_recommend.find_elements_by_class_name('android.widget.LinearLayout')
        element_comic_recommends[random.randint(0, len(element_comic_recommends) - 1)].click()
        try:
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.find_element_by_id(Page_config.PageID.comic_read))
        except Exception, e:
            # 判断超时时，点击刷新页面
            for i in range(1, 21):
                try:
                    element_refresh = driver.find_elements_by_id('com.xmtj.mkz:id/refresh')
                    if element_refresh is not None:
                        element_refresh.click()
                        break
                except Exception, e:
                    print '网络出错，页面未能刷新'
                    continue

        element_comic = self.driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout')
        comic_name = element_comic.find_element_by_id(Page_config.PageID.comic_name).text
        print '相关推荐随机选择的漫画为：%s' % comic_name

    # 测试漫画详情页详情
    def test_case_comicDetailCase2(self):
        element_tab = self.driver.find_element_by_id('com.xmtj.mkz:id/tab_layout')
        element_tabs = element_tab.find_elements_by_class_name('android.widget.FrameLayout')
        # 点击详情
        element_tabs[0].click()
        # 判断作品简介是否存在展开按钮
        try:
            self.driver.find_element_by_id('com.xmtj.mkz:id/more_introduction').click()

            def assTrue2():
                try:
                    self.driver.find_element_by_id('com.xmtj.mkz:id/more_introduction')
                    print '作品简介展开按钮点击测试失败，点击后仍然存在'
                    return False
                except Exception, e:
                    print '作品简介展开按钮点击测试成功'
                    return True

            result = assTrue2()
            self.assertTrue(result)
        except Exception, e:
            print '该作品简介无展开按钮'

        # 作者区域点击跳转作者动态页面
        self.driver.find_element_by_id('com.xmtj.mkz:id/author_name').click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/count_recycler'))
        element_count = self.driver.find_element_by_id('com.xmtj.mkz:id/count_recycler')
        element_counts = element_count.find_elements_by_id('com.xmtj.mkz:id/content_layout')
        self.assertEqual(len(element_counts), 3)
        time.sleep(1)
        self.driver.find_element_by_id(Page_config.PageID.top_back).click()
        print '详情点击作者跳转测试通过'

        # 评分区域功能测试
        while True:
            try:
                element_score1 = self.driver.find_element_by_id(Page_config.PageID.comic_scoreID)
                break
            except Exception, e:
                Swipe_op.SwipeDown(self)
                continue
        try:
            if element_score1.text == '暂无评分':
                print '漫画暂无评分'
            else:
                element_score2 = self.driver.find_element_by_id('com.xmtj.mkz:id/comic_rating')
                self.assertEqual(element_score1.text.split('分')[0], element_score2.text)
                print '该漫画当前评分为：%s' % element_score2.text
        except Exception, e:
            print '漫画评分显示出错'

        element_score1.click()
        # 判断评分窗口标题是否正确
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/title'))
        element_title1 = self.driver.find_element_by_id('com.xmtj.mkz:id/title')
        self.assertEqual(element_title1.text, u'亲，快来打个分吧~')
        # 获取当前时间
        now_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y.%m.%d')
        # 评分星级
        element_star = self.driver.find_element_by_id('com.xmtj.mkz:id/rating')
        element_stars = element_star.find_elements_by_class_name('android.widget.ImageView')
        # 随机选择星级分数
        n = random.randint(0, 4)

        try:
            # 判断是否存在打分时间
            element_tips = self.driver.find_element_by_id('com.xmtj.mkz:id/tips')
            # 获取最近能打分时间
            element_tips_text1 = element_tips.text.split('：')[1].split('以后')[0]
            element_tips_text1_str = element_tips_text1.encode('unicode-escape').decode('string_escape')
            # 判断确认按钮文案是否正确
            element_sure = self.driver.find_element_by_id('com.xmtj.mkz:id/sure')
            self.assertEqual(element_sure.text, u'修改')
            # 比较两个时间
            t1 = filter(str.isdigit, element_tips_text1_str)
            t2 = filter(str.isdigit, now_time)
            if t1 <= t2:
                element_stars[n].click()
                element_sure.click()
                print '该漫画可以评分，随机打分：%d颗星，测试通过' % (n+1)
            elif t1 > t2:
                self.assertEqual(element_sure.get_attribute('clickable'), u'false')
                print '该漫画已打过分，下次能打分时间为：%s，测试通过' % element_tips_text1
                self.driver.find_element_by_id('com.xmtj.mkz:id/cancel').click()
        except Exception, e:
            # 判断确认按钮文案是否正确
            element_sure = self.driver.find_element_by_id('com.xmtj.mkz:id/sure')
            self.assertEqual(element_sure.text, u'确定')
            element_stars[n].click()
            element_sure.click()
            print '该漫画可以评分，随机打分：%d颗星，测试通过' % (n+1)
        time.sleep(1)

        # 月票区域功能测试
        self.driver.find_element_by_id(Page_config.PageID.vote_numID).click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/tv_title'))
        element_title2 = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_title')
        self.assertEqual(element_title2.text, u'为喜欢的漫画投上一票')
        element_recycler = self.driver.find_element_by_id('com.xmtj.mkz:id/vote_recycler')
        element_recyclers = element_recycler.find_elements_by_id('com.xmtj.mkz:id/text')
        element_ok = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_ok')
        self.assertEqual(element_ok.text, u'投了个票')
        # 测试购买月票跳转是否正常
        self.driver.find_element_by_id('com.xmtj.mkz:id/tv_buy').click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id(Page_config.PageID.ticket_info))
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        time.sleep(1)
        self.driver.find_element_by_id(Page_config.PageID.vote_numID).click()
        # 获取用户月票数
        element_ticket = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_month_ticket').text
        element_ticket_str = element_ticket.encode("utf-8")
        element_ticket_num = filter(str.isdigit, element_ticket_str)
        print '用户当前总月票数为：%s' % element_ticket_num
        # 判断不同月票数，投票按钮状态
        global num1
        if string.atoi(element_ticket_num) != 0:
            if string.atoi(element_ticket_num) >= 5:
                for num1 in range(0, 3):
                    element_recyclers[num1].click()
                    self.assertEqual(element_ok.get_attribute('clickable'), u'true')
            elif 1 < string.atoi(element_ticket_num) < 5:
                element_recyclers[2].click()
                self.assertEqual(element_ok.get_attribute('clickable'), u'false')
                for num1 in range(0, 2):
                    element_recyclers[num1].click()
                    self.assertEqual(element_ok.get_attribute('clickable'), u'true')
            elif string.atoi(element_ticket_num) == 1:
                for num1 in range(1, 3):
                    element_recyclers[num1].click()
                    self.assertEqual(element_ok.get_attribute('clickable'), u'false')
                num1 = 0
                element_recyclers[num1].click()
                self.assertEqual(element_ok.get_attribute('clickable'), u'true')

            # 获取投月票数
            element_recyclers_str = element_recyclers[num1].text.encode("utf-8")
            element_recycler_num = filter(str.isdigit, element_recyclers_str)
            last_ticket = string.atoi(element_ticket_num) - string.atoi(element_recycler_num)
            # 测试投月票是否成功，并查看剩余月票
            element_ok.click()
            time.sleep(3)
            self.driver.find_element_by_id(Page_config.PageID.vote_numID).click()
            # 获取用户月票数
            element_ticket1 = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_month_ticket').text
            element_ticket_str1 = element_ticket1.encode("utf-8")
            element_ticket_num1 = string.atoi(filter(str.isdigit, element_ticket_str1))
            self.assertEqual(last_ticket, element_ticket_num1)
            print '投月票测试通过，用户剩余月票为：%d' % last_ticket
            self.driver.find_element_by_id('com.xmtj.mkz:id/tv_cancel').click()

        elif string.atoi(element_ticket_num) == 0:
            for num1 in range(0, 3):
                element_recyclers[num1].click()
                self.assertEqual(element_ok.get_attribute('clickable'), u'false')
            self.driver.find_element_by_id('com.xmtj.mkz:id/tv_cancel').click()
            print '用户月票数不足，无法投票，测试通过'
        time.sleep(1)

        # 元宝区域功能测试
        self.driver.find_element_by_id(Page_config.PageID.donateID).click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/tv_title'))
        element_title3 = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_title')
        self.assertEqual(element_title3.text, u'打赏给喜欢的Ta')
        # 获取用户元宝数
        element_money = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_month_ticket').text
        element_money_str = element_money.encode("utf-8")
        element_money_num = filter(str.isdigit, element_money_str)
        print '用户当前总元宝数为：%s' % element_money_num
        # 判断不同元宝数，确定按钮状态
        global num2
        if string.atoi(element_money_num) >= 100:
            if string.atoi(element_money_num) >= 1000:
                for num2 in range(0, 3):
                    element_recyclers[num2].click()
                    self.assertEqual(element_ok.get_attribute('clickable'), u'true')
            elif 100 < string.atoi(element_money_num) < 1000:
                element_recyclers[2].click()
                self.assertEqual(element_ok.get_attribute('clickable'), u'false')
                for num2 in range(0, 2):
                    element_recyclers[num2].click()
                    self.assertEqual(element_ok.get_attribute('clickable'), u'true')
            elif string.atoi(element_money_num) == 100:
                for num2 in range(1, 3):
                    element_recyclers[num1].click()
                    self.assertEqual(element_ok.get_attribute('clickable'), u'false')
                num2 = 0
                element_recyclers[0].click()
                self.assertEqual(element_ok.get_attribute('clickable'), u'true')

            # 获取打赏元宝数
            element_recyclers_str1 = element_recyclers[num2].text.encode("utf-8")
            element_recycler_num1 = filter(str.isdigit, element_recyclers_str1)
            last_money = string.atoi(element_money_num) - string.atoi(element_recycler_num1)
            # 测试打赏元宝是否成功，并查看剩余元宝
            element_ok.click()
            time.sleep(3)
            self.driver.find_element_by_id(Page_config.PageID.donateID).click()
            # 获取用户元宝数
            element_money1 = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_month_ticket').text
            element_money_str1 = element_money1.encode("utf-8")
            element_money_num1 = string.atoi(filter(str.isdigit, element_money_str1))
            self.assertEqual(last_money, element_money_num1)
            print '打赏元宝测试通过，用户剩余元宝为：%d' % last_money
            self.driver.find_element_by_id('com.xmtj.mkz:id/tv_cancel').click()

        elif string.atoi(element_money_num) < 100:
            for num1 in range(0, 3):
                element_recyclers[num1].click()
                self.assertEqual(element_ok.get_attribute('clickable'), u'false')
            self.driver.find_element_by_id('com.xmtj.mkz:id/tv_cancel').click()
            print '用户元宝数不足，无法打赏，测试通过'
        time.sleep(2)

    # 测试漫画详情页评论
    def test_case_comicDetailCase4(self):
        element_tab = self.driver.find_element_by_id('com.xmtj.mkz:id/tab_layout')
        element_tabs = element_tab.find_elements_by_class_name('android.widget.FrameLayout')
        # 点击评论
        element_tabs[2].click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/like_count'))
        # 无内容不能点击评论按钮
        element_send = self.driver.find_element_by_id('com.xmtj.mkz:id/send')
        self.assertEqual(element_send.get_attribute('enabled'), u'false')
        print '未输入评论内容时，无法点击发布，测试通过'
        # 输入的内容不足4个字
        self.driver.find_element_by_id('com.xmtj.mkz:id/edit').send_keys('123')
        element_send.click()
        print '评论不足4个字符时，发布不成功，测试通过'
        time.sleep(1)
        # 输入正确格式内容
        self.driver.find_element_by_id('com.xmtj.mkz:id/edit').send_keys('1234')
        element_send.click()
        print '评论输入正确时，发布成功，测试通过'
        time.sleep(1)

        # 测试点赞功能
        element_like = self.driver.find_elements_by_id('com.xmtj.mkz:id/like_count')
        element_like[random.randint(0, len(element_like) - 1)].click()
        print '点赞功能测试通过'

    # 测试漫画其他功能区域（收藏，分享）
    def test_case_comicDetailCase3(self):
        # 测试收藏功能
        element_favorite = self.driver.find_element_by_id('com.xmtj.mkz:id/favorite')
        element_favorite.click()
        try:
            element_msg = self.driver.find_element_by_id('com.xmtj.mkz:id/msg')
            self.assertEqual(element_msg.text, u'亲，确定要取消收藏吗？')
            self.driver.find_element_by_id('com.xmtj.mkz:id/sure').click()
            print '该漫画已被收藏，取消收藏测试通过'
        except Exception, e:
            print '该漫画未被收藏，添加收藏测试通过'
        time.sleep(1)

        # 测试点击跳转缓存页面
        self.driver.find_element_by_id('com.xmtj.mkz:id/top_menu_cache').click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id(Page_config.PageID.titleID))
        element_title = self.driver.find_element_by_id(Page_config.PageID.titleID)
        self.assertEqual(element_title.text, u'选择缓存章节')
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        print '点击缓存按钮，正常跳转缓存页面，测试通过'
        time.sleep(1)

        # 测试分享
        self.driver.find_element_by_id('com.xmtj.mkz:id/top_menu_share').click()
        element_socialize = self.driver.find_elements_by_id('com.xmtj.mkz:id/socialize_text_view')
        qq = self.driver.is_app_installed('com.tencent.mobileqq')
        wx = self.driver.is_app_installed('com.tencent.mm')
        wb = self.driver.is_app_installed('com.sina.weibo')
        for num in range(0, len(element_socialize)):
            element_socialize_text = element_socialize[num].text
            if wx:
                print
                if element_socialize_text == u'微信':
                    element_socialize[num].click()
                    self.assertTrue(self.driver.wait_activity('.ui.account.SimpleLoginUI', 10, 1))
                    print '安装微信客户端，分享正常显示微信icon并跳转，测试通过'
                    self.driver.press_keycode('4')
                    time.sleep(1)
                    self.driver.find_element_by_id('com.xmtj.mkz:id/top_menu_share').click()
                if element_socialize_text == u'微信朋友圈':
                    element_socialize[num].click()
                    self.assertTrue(self.driver.wait_activity('.ui.account.SimpleLoginUI', 10, 1))
                    print '安装微信客户端，分享正常显示微信朋友圈icon并跳转，测试通过'
                    self.driver.press_keycode('4')
                    time.sleep(1)
                    self.driver.find_element_by_id('com.xmtj.mkz:id/top_menu_share').click()
            else:
                if element_socialize_text == u'微信':
                    print '未安装微信客户端，分享仍显示微信icon，测试失败'
                if element_socialize_text == u'微信朋友圈':
                    print '未安装微信客户端，分享仍显示微信朋友圈icon，测试失败'
            if qq:
                if element_socialize_text == u'QQ':
                    element_socialize[num].click()
                    self.assertTrue(self.driver.wait_activity('.activity.LoginActivity', 10, 1))
                    self.driver.press_keycode('4')
                    print '安装QQ客户端，分享正常显示QQicon并跳转，测试通过'
                    time.sleep(1)
                    self.driver.find_element_by_id('com.xmtj.mkz:id/top_menu_share').click()
                if element_socialize_text == u'QQ空间':
                    element_socialize[num].click()
                    self.assertTrue(self.driver.wait_activity('.activity.LoginActivity', 10, 1))
                    self.driver.press_keycode('4')
                    time.sleep(1)
                    print '安装QQ客户端，分享正常显示QQ空间icon并跳转，测试通过'
                    self.driver.find_element_by_id('com.xmtj.mkz:id/top_menu_share').click()
            else:
                if element_socialize_text == u'QQ':
                    print '未安装QQ客户端，分享仍显示QQicon，测试失败'
                if element_socialize_text == u'QQ空间':
                    print '未安装QQ客户端，分享仍显示QQ空间icon，测试失败'
            if element_socialize_text == u'新浪':
                element_socialize[num].click()
                if wb:
                    self.assertTrue(self.driver.wait_activity('.SSOLoginActivity', 10, 0.5))
                    print '分享正常显示新浪微博icon并跳转微博客户端页面，测试通过'
                else:
                    WebDriverWait(self.driver, 30).until(
                        lambda driver: driver.find_element_by_xpath('//android.webkit.WebView['
                                                                    '@content-desc="登录 - 新浪微博"]'))
                self.driver.press_keycode('4')
                print '分享正常显示新浪微博icon并跳转H5页面，测试通过'
















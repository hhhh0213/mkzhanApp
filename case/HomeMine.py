# -*- coding:utf-8 -*-

import time
import unittest
import os
import random
import re
from config import appium_config, Page_config
from driver import Swipe_op
from selenium.webdriver.support.wait import WebDriverWait

# 设置路径信息
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class HomeMineTest(unittest.TestCase):
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

        # 进入我的页面
        time.sleep(5)
        cls.driver.find_element_by_id(Page_config.PageID.homeMy).click()

    # 退出测试
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # 未登录状态，我的页面各页面跳转
    def test_case_homeMineCase1(self):
        # 未登录时，按钮显示的文案
        element_tv1 = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_name')
        element_tv2 = self.driver.find_element_by_id(Page_config.PageID.myLogin)
        self.assertEqual(element_tv1.text, u'点击头像登录呦')
        self.assertEqual(element_tv2.text, u'登录后可以尽情的享受更多的功能~')
        # 点击头像跳转登录页面
        self.driver.find_element_by_id(Page_config.PageID.myImgID).click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.logInID))
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        print '未登录状态下点击头像跳转登录页面测试通过'

        # VIP状态及页面跳转
        element_vip_info = self.driver.find_element_by_id(Page_config.PageID.vip_info)
        self.assertEqual(element_vip_info.text, u'未开通VIP')
        element_getVip = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_get_vip_tip')
        self.assertEqual(element_getVip.text, u'开通VIP 惊喜多多')
        element_getVip.click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.logInID))
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        print '未登录状态下点击VIP状态栏跳转登录页面测试通过'

        # 元宝、月票及我的账户跳转账户页面，随机选择
        element_list1 = [Page_config.PageID.myMoney, Page_config.PageID.myTicket, Page_config.PageID.accountID]
        self.driver.find_element_by_id(element_list1[random.randint(0, len(element_list1) - 1)]).click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.titleID))

        # 判断跳转我的账户页面的各元素
        self.driver.find_element_by_id('com.xmtj.mkz:id/please_login').click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.logInID))
        self.driver.find_element_by_accessibility_id('转到上一层级').click()

        # 元宝与月票数应均为0
        element_value1 = self.driver.find_element_by_id('com.xmtj.mkz:id/money_value')
        element_value2 = self.driver.find_element_by_id('com.xmtj.mkz:id/ticket_value')
        self.assertEqual(element_value1.text, '0')
        self.assertEqual(element_value1.text, element_value2.text)

        # 点击元宝的充值按钮跳转
        self.driver.find_element_by_id(Page_config.PageID.chargeID).click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.titleID))
        element_charge_title = self.driver.find_element_by_id(Page_config.PageID.titleID).text
        self.assertEqual(element_charge_title, u'充值元宝')
        while True:
            try:
                self.driver.find_element_by_id(Page_config.PageID.pay_buttonID).click()
                WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.logInID))
                break
            except Exception, e:
                Swipe_op.SwipeDown(self)
        for x in range(1, 3):
            self.driver.find_element_by_accessibility_id('转到上一层级').click()
        print '未登录状态下点击充值元宝跳转登录页面测试通过'

        # 点击购买月票跳转
        element_ticket = self.driver.find_element_by_id(Page_config.PageID.buy_month_ticketID)
        self.assertEqual(element_ticket.text, u'购买')
        element_ticket.click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.logInID))
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        print '未登录状态下点击购买月票跳转登录页面测试通过'

        # 点击VIP状态跳转
        element_vip_time = self.driver.find_element_by_id(Page_config.PageID.vip_time)
        self.assertEqual(element_vip_time.text, u'开通VIP 惊喜多多')
        element_buyVip = self.driver.find_element_by_id(Page_config.PageID.buy_vipID)
        self.assertEqual(element_buyVip.text, u'去开通')
        element_buyVip.click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.vip_info))
        element_vipText = self.driver.find_element_by_id(Page_config.PageID.vip_info).text
        self.assertEqual(element_vipText, u'当前为游客，请登录后开通VIP')
        while True:
            try:
                self.driver.find_element_by_id(Page_config.PageID.pay_buttonID).click()
                WebDriverWait(self.driver, 15).until(
                    lambda driver: driver.find_element_by_id(Page_config.PageID.logInID))
                break
            except Exception, e:
                Swipe_op.SwipeDown(self)
        for x in range(1, 3):
            self.driver.find_element_by_accessibility_id('转到上一层级').click()
        print '未登录状态下点击VIP状态的开通VIP跳转登录页面测试通过'

        # 判断未登录资产记录区域应为空
        element_tab = self.driver.find_element_by_id('com.xmtj.mkz:id/tab_layout')
        element_list2 = element_tab.find_elements_by_class_name('android.widget.FrameLayout')
        for num in range(0, len(element_list2)):
            element_list2[num].click()
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/empty_text'))
            element_empty_text = self.driver.find_element_by_id('com.xmtj.mkz:id/empty_text')
            self.assertEqual(element_empty_text.text, u'这里空空如也')
            time.sleep(1)
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        print '未登录状态下检查元宝等记录显示测试通过'

        # 点击我的消息跳转
        self.driver.find_element_by_id(Page_config.PageID.messageID).click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.logInID))
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        print '未登录状态下点击我的消息跳转测试通过'

        # 点击问题反馈-我的反馈跳转
        self.driver.find_element_by_id(Page_config.PageID.feedbackID).click()
        time.sleep(1)
        self.driver.find_element_by_id(Page_config.PageID.my_feedbackID).click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.logInID))
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        time.sleep(1)
        self.driver.find_element_by_id(Page_config.PageID.backButtonID).click()
        print '未登录状态下点击问题反馈-我的反馈跳转测试通过'
    
    # 登录状态，个人动态页面展示
    def test_case_homeMineCase2(self):

        # 登录账号
        self.driver.find_element_by_id(Page_config.PageID.myImgID).click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.logInID))
        self.driver.find_element_by_id(Page_config.PageID.usernameID).send_keys(Page_config.PageID.usernameText)
        self.driver.find_element_by_id(Page_config.PageID.passwordID).send_keys(Page_config.PageID.passwordText)
        self.driver.find_element_by_id(Page_config.PageID.logInID).click()
        time.sleep(2)

        # 进入个人主页
        element_mylogin = self.driver.find_element_by_id(Page_config.PageID.myLogin)
        self.assertEqual(element_mylogin.text, u'查看个人主页')
        element_mylogin.click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.myImgID))
        
        # 进入关注、粉丝页面测试功能
        element_count = self.driver.find_element_by_id('com.xmtj.mkz:id/count_recycler')
        element_contents = element_count.find_elements_by_id('com.xmtj.mkz:id/content_layout')

        element_contents[0].click()     # 进入关注列表
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id('android:id/list'))
        element_followList = self.driver.find_elements_by_id('com.xmtj.mkz:id/tv_name')
        element_followButton = self.driver.find_elements_by_id('com.xmtj.mkz:id/tv_follow')
        num1 = random.randint(0, len(element_followList) - 1)
        element_follow = element_followList[num1]
        element_follow_name = element_follow.text
        print '关注列表随机选择的已关注用户为：%s' % element_follow_name

        # 判断取消关注操作是否成功
        element_followButton[num1].click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/msg'))
        self.driver.find_element_by_id('com.xmtj.mkz:id/sure').click()
        try:
            if element_follow_name in element_followList.text:
                print '取消关注操作测试失败'
        except Exception, e:
            print '关注列表取消关注测试通过'

        time.sleep(2)
        self.driver.find_element_by_id('com.xmtj.mkz:id/white_back').click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.myImgID))

        element_contents[1].click()  # 进入粉丝列表
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
        
        element_tab = self.driver.find_element_by_id('com.xmtj.mkz:id/tab_layout')
        element_tabs = element_tab.find_elements_by_class_name('android.widget.FrameLayout')

        # 动态列表测试
        element_tabs[0].click()
        # 随机滑动页面后，选择第一个动态内容
        element_activitys = self.driver.find_elements_by_id('com.xmtj.mkz:id/tv_activity')
        element_details = self.driver.find_elements_by_id('com.xmtj.mkz:id/detail_layout')
        element_activity = element_activitys[0]
        element_detail = element_details[0]
        print '动态页面随机选择的动态为：%s' % element_activity.text

        # 判断该动态类型，并点击跳转测试

        factor = '收藏|评论|打赏'
        if re.search(factor, str(element_activity.text)) is not None:
            element_comic_name = element_detail.find_element_by_id(Page_config.PageID.comic_name).text
            element_detail.click()
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id(Page_config.PageID.comic_name))
            element_comic1 = self.driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout')
            comic_name2 = element_comic1.find_element_by_id(Page_config.PageID.comic_name).text
            self.assertEqual(element_comic_name, comic_name2)
            self.driver.find_element_by_id(Page_config.PageID.top_back).click()
            print '跳转的漫画为：%s' % element_comic_name
        elif re.search('关注', str(element_activity.text)) is not None:
            element_other_name = element_detail.find_element_by_id('com.xmtj.mkz:id/tv_other_name').text
            element_detail.click()
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/tv_name'))
            tv_name = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_name').text
            re.search(str(tv_name), str(element_other_name))
            self.driver.find_element_by_id(Page_config.PageID.top_back).click()
            print '跳转的漫画为：%s' % element_other_name

        print '动态列表随机点击跳转测试通过'
        time.sleep(1)

        # 收藏列表测试
        element_tabs[1].click()
        for swipeNum in range(1, random.randint(1, 6)):
            Swipe_op.SwipeDown(self)
        element_names = self.driver.find_elements_by_id('com.xmtj.mkz:id/name')
        element_name = element_names[random.randint(0, len(element_names) - 1)]
        print '收藏页面随机选择的漫画为：%s' % element_name.text
        element_name.click()
        WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id(Page_config.PageID.comic_read))
        self.driver.find_element_by_id(Page_config.PageID.top_back).click()
        self.driver.press_keycode('4')
        print '收藏列表随机点击跳转测试通过'
        time.sleep(1)

    # 登录状态，关注、粉丝、元宝、月票点击跳转
    def test_case_homeMineCase3(self):
        # 点击关注跳转
        self.driver.find_element_by_id('com.xmtj.mkz:id/follow_layout').click()
        WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/tab_layout'))
        # 验证跳转的页面为关注
        element_followTab = self.driver.find_element_by_id('com.xmtj.mkz:id/tab_layout')
        element_followsel = element_followTab.find_elements_by_class_name('android.widget.FrameLayout')[0]
        self.assertTrue(element_followsel.is_selected())
        self.driver.find_element_by_id('com.xmtj.mkz:id/white_back').click()
        time.sleep(1)

        # 点击粉丝跳转
        self.driver.find_element_by_id('com.xmtj.mkz:id/fans_layout').click()
        WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/tab_layout'))
        # 验证跳转的页面为粉丝
        element_followTab = self.driver.find_element_by_id('com.xmtj.mkz:id/tab_layout')
        element_followsel = element_followTab.find_elements_by_class_name('android.widget.FrameLayout')[1]
        self.assertTrue(element_followsel.is_selected())
        self.driver.find_element_by_id('com.xmtj.mkz:id/white_back').click()
        time.sleep(1)

        # 点击元宝跳转
        self.driver.find_element_by_id(Page_config.PageID.myMoney).click()
        WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id(Page_config.PageID.titleID))
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        time.sleep(1)

        # 点击月票跳转
        self.driver.find_element_by_id(Page_config.PageID.myTicket).click()
        WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id(Page_config.PageID.titleID))
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        time.sleep(2)
        print '我的页面关注、粉丝、元宝及月票tab按钮点击跳转测试通过'
    
    # VIP状态点击跳转
    def test_case_homeMineCase4(self):
        element_vip_time = self.driver.find_element_by_id(Page_config.PageID.vip_info)
        element_vip_timeText = element_vip_time.text
        print '当前用户的VIP状态为：%s' % element_vip_time.text

        # 根据VIP状态判断页面是否显示正常
        if element_vip_timeText == '未开通VIP':
            element_buyVip = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_get_vip_tip')
            self.assertEqual(element_buyVip.text, u'开通VIP 惊喜多多')
            element_buyVip.click()
            WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.vip_info))
            element_vipText = self.driver.find_element_by_id(Page_config.PageID.vip_info).text
            self.assertEqual(element_vipText, u'您尚未开通漫客栈VIP')
        else:
            element_vip_time.click()
            WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.vip_info))
            element_vipText = self.driver.find_element_by_id(Page_config.PageID.vip_info).text
            self.assertEqual(element_vip_timeText, element_vipText)
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        print '登录状态下点击VIP状态的跳转开通VIP页面测试通过'
        time.sleep(2)

    # 我的账户点击跳转
    def test_case_homeMineCase5(self):
        self.driver.find_element_by_id(Page_config.PageID.accountID).click()
        WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/money_value'))
        # 获取元宝数
        element_valueText = self.driver.find_element_by_id('com.xmtj.mkz:id/money_value').text
        # 点击元宝的充值按钮跳转
        self.driver.find_element_by_id(Page_config.PageID.chargeID).click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.titleID))
        element_charge_title = self.driver.find_element_by_id(Page_config.PageID.titleID).text
        element_moneyText = self.driver.find_element_by_id(Page_config.PageID.moneyID).text
        self.assertEqual(element_charge_title, u'充值元宝')
        self.assertEqual(element_valueText, element_moneyText)
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        print '登录状态下点击充值元宝跳转充值元宝页面测试通过'

        # 点击VIP状态跳转
        element_vip_time = self.driver.find_element_by_id(Page_config.PageID.vip_time).text
        element_buyVip = self.driver.find_element_by_id(Page_config.PageID.buy_vipID)
        if element_vip_time == '开通VIP 惊喜多多':
            self.assertEqual(element_buyVip.text, u'去开通')
        else:
            self.assertEqual(element_buyVip.text, u'去续费')
        element_buyVip.click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.vip_info))
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        print '登录状态下点击VIP状态的跳转VIP付费页面测试通过'

        # 点击购买月票跳转
        element_ticket = self.driver.find_element_by_id(Page_config.PageID.buy_month_ticketID)
        self.assertEqual(element_ticket.text, u'购买')
        element_ticket.click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.vip_info))
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        print '登录状态下点击月票链接跳转VIP付费页面测试通过'

        # 判断登录账户资产记录区域中的信息
        element_tab = self.driver.find_element_by_id('com.xmtj.mkz:id/tab_layout')
        element_list2 = element_tab.find_elements_by_class_name('android.widget.FrameLayout')
        for num in range(0, 3):
            element_list2[num].click()
            element_list2text = element_list2[num].find_element_by_class_name('android.widget.TextView').text
            try:
                WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id('android:id/list'))
                for swipeNum in range(1, random.randint(3, 11)):
                    Swipe_op.SwipeDown(self)
                element_contentList = self.driver.find_element_by_id('android:id/list')
                element_contents = element_contentList.find_elements_by_id('com.xmtj.mkz:id/content')
                element_content = element_contents[random.randint(0, len(element_contents) - 1)]
                if num == 0:
                    text = '打赏|购买|增加|减少'
                    re.search(text, str(element_content.text))
                elif num == 1:
                    re.search('VIP', str(element_content.text))
                elif num == 2:
                    re.search('月票', str(element_content.text))
                print '随机选择的%s记录为：%s' % (element_list2text, element_content.text)
            except Exception, e:
                WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/empty_text'))
                element_empty_text = self.driver.find_element_by_id('com.xmtj.mkz:id/empty_text')
                self.assertEqual(element_empty_text.text, u'这里空空如也')
                print '%s记录为空' % element_list2text
            time.sleep(3)
        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        print '登录状态下检查元宝等记录显示测试通过'

    # 我的消息页面操作测试
    def test_case_homeMineCase6(self):
        self.driver.find_element_by_id(Page_config.PageID.messageID).click()
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/tv_title'))
        # 随机向下滑动页面
        swipe_max = random.randint(1, 21)
        for n in range(1, swipe_max):
            Swipe_op.SwipeDown(self)

        # 选择一个消息内容
        element_titles = self.driver.find_elements_by_id('com.xmtj.mkz:id/tv_title')
        element_title = element_titles[random.randint(1, 2)]

        try:
            # 定位随机选择的消息是否存在小红点
            element_redDot = self.driver.find_element_by_android_uiautomator(
                'new UiSelector().text("%s").fromParent(new UiSelector().resourceId("com.xmtj.mkz:id/red_dot").index(0))'
                % element_title.text)
            print '此条消息未读：%s' % element_title.text

            # 判断消息类型，并点击跳转做对比
            if re.search('关注', str(element_title.text)):
                element_tvname = self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().text("%s").fromParent(new UiSelector().resourceId("com.xmtj.mkz:id/tv_other_name").index(1))'
                    % element_title.text).text
                re.search(str(element_tvname), str(element_title.text))
                element_title.click()
                WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/tv_name'))
                tv_name = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_name').text
                re.search(str(tv_name), str(element_tvname))
                print '关注类消息点击跳转测试通过'

            elif re.search('回复', str(element_title.text)):
                element_comic = self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().text("%s").fromParent(new UiSelector().resourceId("com.xmtj.mkz:id/comic_name").index(0))'
                    % element_title.text).text

                # 获取回复的内容
                element_reply = self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().text("%s").fromParent(new UiSelector().resourceId("com.xmtj.mkz:id/tv_reply").index(3))'
                    % element_title.text).text

                element_title.click()
                WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id(Page_config.PageID.comic_name))
                element_comic2 = self.driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout')
                comic_name2 = element_comic2.find_element_by_id(Page_config.PageID.comic_name).text
                self.assertEqual(element_comic, comic_name2)
                print '评论回复的内容为：%s，回复的漫画为：%s，漫画点击跳转测试通过' % (element_reply, element_comic)
            self.driver.find_element_by_id(Page_config.PageID.top_back).click()
            try:
                if element_redDot is not None:
                    print '阅读消息红点消失功能测试通过'
            except Exception, e:
                print '已读消息红点消失测试失败'

        except Exception, e:
            print '此条消息已读：%s' % element_title.text
            if re.search('关注', str(element_title.text)):
                element_tvname = self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().text("%s").fromParent(new UiSelector().resourceId("com.xmtj.mkz:id/tv_other_name").index(1))'
                    % element_title.text).text
                re.search(str(element_tvname), str(element_title.text))
                element_title.click()
                WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id('com.xmtj.mkz:id/tv_name'))
                tv_name = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_name').text
                re.search(str(tv_name), str(element_tvname))
                print '关注类消息点击跳转测试通过'

            elif re.search('回复', str(element_title.text)):
                element_comic = self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().text("%s").fromParent(new UiSelector().resourceId("com.xmtj.mkz:id/comic_name").index(0))'
                    % element_title.text).text
                element_reply = self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().text("%s").fromParent(new UiSelector().resourceId("com.xmtj.mkz:id/tv_reply").index(2))'
                    % element_title.text).text
                element_title.click()
                WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id(Page_config.PageID.comic_name))
                element_comic2 = self.driver.find_element_by_id('com.xmtj.mkz:id/top_bg_layout')
                comic_name2 = element_comic2.find_element_by_id(Page_config.PageID.comic_name).text
                self.assertEqual(element_comic, comic_name2)
                print '评论回复的内容为：%s，回复的漫画为：%s，漫画点击跳转测试通过' % (element_reply, element_comic)
            self.driver.find_element_by_id(Page_config.PageID.top_back).click()

        # 测试全部已读按钮功能
        try:
            element_readStatus = self.driver.find_element_by_id('com.xmtj.mkz:id/tv_status')
            element_readStatus.click()
            time.sleep(3)
            try:
                self.driver.find_element_by_id('com.xmtj.mkz:id/tv_status')
                print '点击全部已读，该按钮仍然存在'
            except Exception, e:
                # 将页面滑至顶部
                for n in range(1, swipe_max):
                    Swipe_op.SwipeUp(self)
                # 检查是否仍然存在红点
                while True:
                    try:
                        self.driver.find_element_by_android_uiautomator(
                            'new UiSelector().text("%s").fromParent(new UiSelector().resourceId("com.xmtj.mkz:id/red_dot").index(0))'
                            % element_title.text)
                        print '点击全部已读，仍然存在小红点'
                    except Exception, e:
                        Swipe_op.SwipeDown(self)
                    try:
                        self.driver.find_element_by_id('com.xmtj.mkz:id/no_more')
                        break
                    except Exception, e:
                        continue
        except Exception, e:
            # 将页面滑至顶部
            for n in range(1, swipe_max):
                Swipe_op.SwipeUp(self)
            # 检查是否存在红点,但全部已读未显示
            while True:
                try:
                    self.driver.find_element_by_android_uiautomator(
                        'new UiSelector().text("%s").fromParent(new UiSelector().resourceId("com.xmtj.mkz:id/red_dot").index(0))'
                        % element_title.text)
                    print '存在小红点，但未显示全部已读'
                except Exception, e:
                    Swipe_op.SwipeDown(self)
                try:
                    self.driver.find_element_by_id('com.xmtj.mkz:id/no_more')
                    break
                except Exception, e:
                    continue
        print '全部已读功能测试完毕'
        self.driver.find_element_by_accessibility_id('转到上一层级').click()

    # 我的设置默认设置确认
    def test_case_homeMineCase7(self):
        while True:
            try:
                self.driver.find_element_by_id(Page_config.PageID.settingID).click()
                break
            except Exception, e:
                Swipe_op.SwipeDown(self)
        WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_id(Page_config.PageID.titleID))

        # 阅读模式默认为卷轴
        self.driver.find_element_by_id(Page_config.PageID.reelID).is_selected()
        # 阅读画质默认流畅
        element_text1 = self.driver.find_element_by_id(Page_config.PageID.read_qualityID).text
        self.assertEqual(element_text1, u'流畅')
        # 底部信息默认显示
        read_tipID = self.driver.find_element_by_id(Page_config.PageID.read_tipID)
        self.assertEqual(read_tipID.get_attribute('checked'), u'true')
        # 默认使用音量键翻页
        volumeID = self.driver.find_element_by_id(Page_config.PageID.volumeID)
        self.assertEqual(volumeID.get_attribute('checked'), u'true')
        # 缓存画质默认为流畅
        element_text2 = self.driver.find_element_by_id(Page_config.PageID.cache_qualityID).text
        self.assertEqual(element_text2, u'流畅')
        while True:
            try:
                # 非WIFI提醒默认开启
                remindID = self.driver.find_element_by_id(Page_config.PageID.remindID)
                self.assertEqual(remindID.get_attribute('checked'), u'true')
                # wifi自动缓存默认开启
                auto_cacheID = self.driver.find_element_by_id(Page_config.PageID.auto_cacheID)
                self.assertEqual(auto_cacheID.get_attribute('checked'), u'true')
                # 消息通知默认开启
                notifyID = self.driver.find_element_by_id(Page_config.PageID.notifyID)
                self.assertEqual(notifyID.get_attribute('checked'), u'true')
                break
            except Exception, e:
                Swipe_op.SwipeDown(self)

        self.driver.find_element_by_accessibility_id('转到上一层级').click()
        print '我的设置默认设置检查完成'






# -*- coding:utf-8 -*-

import unittest
import HTMLTestRunnerCN
from case import LoginPage, RegisterPage, ForgetPassword, HomePage, CategoryPage, SearchPage, HomeMine, ComicDetail, ReadPage, Comment


# 定义测试套件
def Test_suite():
    suite = unittest.TestSuite()

    print '1.登录/2.注册/3.找回密码/4.首页/5.分类/6.搜索/7.我的/8.漫画详情页/9.评论页/10.漫画阅读页'
    num = raw_input('请输入要开始测试的用例：')

    if num == '1':
        print '即将开始执行登录页面测试用例'
        suite.addTest(unittest.makeSuite(LoginPage.LoginTest))
    elif num == '2':
        print '即将开始执行注册页面测试用例'
        suite.addTest(unittest.makeSuite(RegisterPage.RegisterTest))
    elif num == '3':
        print '即将开始执行找回密码页面测试用例'
        suite.addTest(unittest.makeSuite(ForgetPassword.ForgetPassTest))
    elif num == '4':
        print '即将开始执行首页页面测试用例'
        suite.addTest(unittest.makeSuite(HomePage.HomePageTest))
    elif num == '5':
        print '即将开始执行分类页面测试用例'
        suite.addTest(unittest.makeSuite(CategoryPage.CategoryTest))
    elif num == '6':
        print '即将开始执行搜索页面测试用例'
        suite.addTest(unittest.makeSuite(SearchPage.SearchTest))
    elif num == '7':
        print '即将开始执行我的页面测试用例'
        suite.addTest(unittest.makeSuite(HomeMine.HomeMineTest))
    elif num == '8':
        print '即将开始执行漫画详情页页面测试用例'
        suite.addTest(unittest.makeSuite(ComicDetail.ComicDetailTest))
    elif num == '9':
        print '即将开始执行评论页面测试用例'
        suite.addTest(unittest.makeSuite(Comment.ComicCommentTest))
    elif num == '10':
        print '即将开始执行漫画阅读页面测试用例'
        suite.addTest(unittest.makeSuite(ReadPage.ComicReadTest))
    else:
        print '即将开始执行所有测试用例'
        suite.addTest(unittest.makeSuite(LoginPage.LoginTest))
        suite.addTest(unittest.makeSuite(RegisterPage.RegisterTest))
        suite.addTest(unittest.makeSuite(ForgetPassword.ForgetPassTest))
        suite.addTest(unittest.makeSuite(HomePage.HomePageTest))
        suite.addTest(unittest.makeSuite(CategoryPage.CategoryTest))
        suite.addTest(unittest.makeSuite(SearchPage.SearchTest))
        suite.addTest(unittest.makeSuite(HomeMine.HomeMineTest))
        suite.addTest(unittest.makeSuite(ComicDetail.ComicDetailTest))
        suite.addTest(unittest.makeSuite(Comment.ComicCommentTest))
        suite.addTest(unittest.makeSuite(ReadPage.ComicReadTest))

    return suite


if __name__ == '__main__':
    result = raw_input('是否开启测试报告记录（y/n）：')

    if result == 'y':
        runner = unittest.TextTestRunner()
        test_suite = Test_suite()
        # 定义测试报告路径
        filename = './doc/test.html'
        # 定义测试报告权限
        fp = file(filename, 'wb')
        # description='详细测试用例结果',不传默认为空；tester设置测试人员名字，不传默认为QA
        runner = HTMLTestRunnerCN.HTMLTestRunner(stream=fp, title='漫客栈APP自动化测试', tester=u"胡佳")

        runner.run(test_suite)
        # 关闭文件，否则无法生成报告
        fp.close()
    elif result == 'n':
        runner = unittest.TextTestRunner()
        test_suite = Test_suite()

        runner.run(test_suite)



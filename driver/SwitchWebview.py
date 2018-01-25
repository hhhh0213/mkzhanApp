# coding: utf-8


def Switch_webview(self):
    webview = self.driver.contexts
    for context in webview:
        if 'WEBVIEW' in context:
            self.driver.switch_to.context(context)
            break

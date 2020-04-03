import time
from tqdm import tqdm
from PIL import Image, ImageEnhance
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions

def login(username,password):
    url='http://i.mooc.chaoxing.com/space/index?'
    browser.get(url)
    browser.find_element_by_id('unameId').send_keys(username)
    browser.find_element_by_id('passwordId').send_keys(password)
    location=browser.find_element_by_id('numVerCode').location
    screenImg = "code.png"
    browser.get_screenshot_as_file(screenImg)
    # size=browser.find_element_by_id('numVerCode').size
    # # #browser.maximize_window()
    # # top = location['y']+90
    # # bottom = location['y'] + size['height']+95
    # # left=location['x']+140
    # # right = location['x'] + size['width']+190
    #
    # #小窗口
    # top = location['y']+90
    # bottom = location['y'] + size['height']+95
    # left=location['x']+90
    # right = location['x'] + size['width']+110
    # img = Image.open(screenImg).crop((left, top, right, bottom))
    # # img = img.convert('RGBA')  # 转换模式：L | RGB
    # # img = img.convert('L')  # 转换模式：L | RGB
    # # img = ImageEnhance.Contrast(img)  # 增强对比度
    # # img = img.enhance(2.0)  # 增加饱和度
    # img.save(screenImg)
    # img.show()
    x=Image.open('code.png')
    Image._show(x)
    code=input('请输入验证码：')
    browser.find_element_by_id('numcode').send_keys(code)
    browser.find_element_by_css_selector('.zl_btn_right').click()
    print('登陆成功')

def task():
    browser.switch_to_frame('frame_content')
    all_lessons=browser.find_elements_by_xpath('//li[@style="position:relative"]//div[@class="Mconright httpsClass"]')
    print(len(all_lessons))
    for t in range(len(all_lessons)):
        # try:
        print('开始进入第%d个课程' %(t+1))
        lesson=all_lessons[t]
        title=lesson.find_element_by_xpath('.//h3//a')
        title=title.get_attribute('title')
        print(title)
        lesson.find_element_by_xpath('.//h3//a').click()

        time.sleep(1)
        n = browser.window_handles # 获取当前页句柄
        browser.switch_to.window (n[1])
        browser.find_element_by_link_text('任务').click()
        n = browser.window_handles # 获取当前页句柄
        browser.switch_to.window (n[2])
        all_div=browser.find_elements_by_xpath('//div[@class="Mct"]')
        print('开始进入签到界面')
        if len(all_div) == 0:
            print('您当前课程无签到任务')
        else:
            for i in tqdm(range(len(all_div))):
                try:
                    div=all_div[i]
                    div.find_element_by_xpath('.//dl').click()
                    time.sleep(1)
                    browser.back()
                except:
                    all_div = browser.find_elements_by_xpath('//div[@class="Mct"]')
                    div=all_div[i]
                    div.find_element_by_xpath('.//dl').click()
                    time.sleep(1)
                    browser.back()
        print(title+'签到遍历完成')
        browser.close()
        n = browser.window_handles # 获取当前页句柄
        #print(n)
        browser.switch_to.window (n[1])
        browser.close()
        n = browser.window_handles # 获取当前页句柄
        browser.switch_to.window (n[0])
        print('第%d个课程签到结束\n' %(t+1))
        browser.refresh()
        time.sleep(1)
        browser.switch_to_frame('frame_content')
        all_lessons = browser.find_elements_by_xpath(
            '//li[@style="position:relative"]//div[@class="Mconright httpsClass"]')
    print('所有课程签到已经结束！')
if __name__ == '__main__':
    opt = ChromeOptions()
    opt.headless = True  # 把Chrome设置成可视化无界面模式，windows/Linux 皆可
    browser=Chrome(options=opt)
    username=input('请输入您的账号：')
    passwd=input('请输入您的密码：')
    login(username,passwd)
    task()

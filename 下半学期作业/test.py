from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import winsound

errorlist = []

def nextpage(driver):
    driver.implicitly_wait(30)
    ele = driver.find_elements_by_class_name('n')
    # ele = driver.find_elements_by_link_text('下一页&gt;')
    if len(ele) == 2:
        driver.implicitly_wait(30)
        time.sleep(2)
        ele[1].click()
    else:
        driver.implicitly_wait(30)
        time.sleep(2)
        ele[0].click()

def initdriver(browser):
    if browser == 'firefox':
        driver = webdriver.Firefox(executable_path='C:/Program Files/Mozilla Firefox/geckodriver.exe')
    else:
        driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')

    driver.get("http://www.baidu.com")
    # assert "Python" in driver.title
    time.sleep(50)  # leave time to login by cell phone
    elem = driver.find_element_by_name("wd")
    elem.clear()
    elem.send_keys("site:nju.edu.cn")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    return driver,browser

def trim(string):
    return ''.join(string.split())

errortitle = ''
def operate(driver, browser):
    errorlist = []
    for i in range(1):
        if i != 0:
            nextpage(driver)
        driver.implicitly_wait(30)
        time.sleep(5)
        elems = driver.find_elements_by_class_name("t")
        for i in range(len(elems)):
            # print(item.text)
            txt = (elems[i].text)
            txt1 = ''
            if i > 0:
                txt1 = (elems[i - 1].text)

            try:
                link = driver.find_element_by_link_text(txt)
                link.click()

                driver.implicitly_wait(30)
                time.sleep(5)
                handles = driver.window_handles
                driver.switch_to.window(handles[1])

                url = driver.current_url
                content = trim(driver.title)

                error = ''
                if url.find('https') == -1:
                    error = error + ',WARNING0'
                else:
                    error = error + ','

                if browser == 'firefox':
                    if trim(content) != trim(txt1) and trim(content) != trim(txt):
                        error = error + ',ERROR0'
                    else:
                        error = error + ','
                else:
                    if trim(content) != trim(txt):
                        error = error + ',ERROR0'
                    else:
                        error = error + ','

                if url.find('nju.edu.cn') == -1:
                    error = error + ',ERROR1,'
                else:
                    error = error + ',,'
                driver.close()
                driver.switch_to.window(handles[0])
                time.sleep(5)
                if error != '':
                    info = txt + ',' + url + error + '\n'
                    errorlist.append(info)
                    print(info)

            except BaseException:
                print(driver.window_handles)
                info = txt + ',' + url + ',,,,ERROR2\n'
                errorlist.append(info)
                print(info)
                handles = driver.window_handles
                if len(handles) == 2:
                    driver.switch_to.window(handles[1])
                    driver.close()
                    driver.switch_to.window(handles[0])
                else:
                    driver.switch_to.window(handles[0])
                print('exception occured on ', txt)
                winsound.Beep(3600, 1000)

    driver.quit()
    return errorlist

def writeTocsv(errorlist, browser):
    with open(str('errorlist-'+browser+'.csv'), 'w',encoding='utf-8') as f:
        f.writelines(errorlist)



if __name__ == '__main__':
    print('错误警告列表提示：\nERROR0:title不符合\nERROR1:网页连接错误\n'
          'ERROR2:网页加载超时\nWARNING0:网页未使用https加密\n')
    ffdriver, ffbrowser = initdriver('firefox')
    el1 = operate(ffdriver, ffbrowser)
    chromedriver,chromebrowser = initdriver('chrome')
    writeTocsv(el1, ffbrowser)
    winsound.Beep(3600, 60*1000)
    el2 = operate(chromedriver,chromebrowser)
    # print(el1)
    # print(el2)
    writeTocsv(el2, chromebrowser)



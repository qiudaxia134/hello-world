from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as pq
import time


def parse_website():
    # 通过Chrome()方法打开chrome浏览器
    browser = webdriver.Chrome()
    # 访问京东网站
    browser.get("https://www.jd.com")
    # 等待50秒
    wait = WebDriverWait(browser, 50)
    # 通过css选择器的id属性获得输入框。until方法表示浏览器完全加载到对应的节点，才返回相应的对象。presence_of_all_elements_located是通过css选择器加载节点
    input = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#key'))
    )

    # 写入要查询的宝贝
    input[0].send_keys('美食')
    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.button'))
    )
    # 点击查询按钮
    submit_button.click()

    # 下滑到底部操作
    for i in range(0, 3):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # 商品列表的总页数
    total = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > em:nth-child(1) > b')
        )
    )
    html = browser.page_source.replace('xmlns', 'another_attr')
    parse_book(1, html)

    for page_num in range(2, int(total[0].text) + 1):
        parse_next_page(page_num, browser, wait)


#解析下一页
def parse_next_page(page_num, browser, wait):
    next_page_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.pn-next > em'))
    )
    next_page_button.click()

    # 滑动到页面底部，用于加载数据
    for i in range(0, 3):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

    # 一页显示60个商品，"#J_goodsList > ul > li:nth-child(60)确保60个商品都正常加载出来。
    wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#J_goodsList > ul > li:nth-child(60)"))
    )
    # 判断翻页成功，当底部的分页界面上显示第几页时，就显示翻页成功。
    wait.until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#J_bottomPage > span.p-num > a.curr"), str(page_num))
    )

    html = browser.page_source.replace('xmlns', 'another_attr')
    parse_book(page_num, html)


def parse_book(page, html):
    doc = pq(html)
    li_list = doc('.gl-item').items()
    print('【-------------------第' + str(page) + '页的宝贝信息---------------------】')
    for item in li_list:
        image_html = item('.gl-i-wrap .p-img')
        book_img_url = item.find('img').attr('data-lazy-img')
        if book_img_url == "done":
            book_img_url = item.find('img').attr('src')
        item('.p-name').find('font').remove()
        book_name = item('.p-name').find('em').text()
        price = item('.p-price').find('em').text() + str(item('.p-price').find('i').text())
        commit = item('.p-commit').find('strong').text()
        shopnum = item('.p-shop').find('a').text()
        text = '店铺名字：' + shopnum +'\n'+ '宝贝标题：' + book_name + '\n'+ '价格：' + price + '\n'+ '评价数量：' + commit +'\n'+  '图片地址:' + book_img_url+'\n'
        print(text, '\n')
        print('-----------------------------------------------------------------------')



def main():
    parse_website()


if __name__ == "__main__":
    main()

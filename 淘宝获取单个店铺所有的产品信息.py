from selenium import webdriver
import time
import mysql.connector
from selenium.webdriver.common.action_chains import ActionChains
import requests
class taobao():
    def __init__(self):
        self.next_page_css = '#J_ShopSearchResult > div > div.shop-hesper-bd.grid > div.pagination > a.J_SearchAsync.next'
        self.link_css = '#J_ShopSearchResult > div > div.shop-hesper-bd.grid > div:nth-child(2) > dl:nth-child(1) > dd.detail > a'
        self.main_pic_css = '#J_ShopSearchResult > div > div.shop-hesper-bd.grid > div:nth-child(2) > dl:nth-child(1) > dd.detail > a'
    def insert_mysql(self):


        mydb = mysql.connector.connect(
            host="localhost",
            user="root",

            database="taobao"
        )

        mycursor = mydb.cursor()

        sql="insert into blender_plugin (name,sales,price,url,comment) values (%s,%s,%s,%s,%s) "
        val=self.super_list
        mycursor.executemany(sql,val)
        mydb.commit()

    def browser_init(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_argument("user-data-dir=C:\\Users\\肖洪才\\.PyCharmCE2019.2\\config\\scratches\\selenium\\selenium")
        self.options.add_argument("start-maximized")
        self.browser=webdriver.Chrome(options=self.options,executable_path=r'C:\Users\肖洪才\AppData\Local\Programs\Python\Python37-32\Scripts\chromedriver.exe')

        url='https://shop113743284.taobao.com/search.htm?spm=2013.1.w4010-8786792875.3.3dde24ddxEHpmA&search=y&orderType=hotsell_desc'
        self.browser.get(url)
        self.browser.maximize_window()
        self.browser.implicitly_wait(8)
        # if self.browser.switch_to.frame('sufei-dialog-content'):
        #
        #     self.browser.find_element_by_css_selector('#TPL_password_1').send_keys('Xhc654477358')
        #     time.sleep(2)
        #     self.browser.find_element_by_css_selector('#J_SubmitStatic').click()
        self.browser.implicitly_wait(10)


    def get_data(self):

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            database="taobao"
        )

        mycursor = mydb.cursor()

        self.general_ID=[]
        self.general_url_list=[]

        mycursor.execute("SELECT URL,ID FROM blender_plugin ")

        myresult = mycursor.fetchall()
        for i in myresult:
            self.general_url_list.append(i[0])
            self.general_ID.append(i[1])






    def engine(self):


        self.browser_init()

        def get_current_infos():
            url_list=[i.get_attribute('href') for i in self.browser.find_elements_by_css_selector('a[class="item-name J_TGoldData"]')]
            # print(url_list)
            name_list=[i.get_attribute('alt') for i in self.browser.find_elements_by_css_selector('a[class="J_TGoldData"] img')]
            # print(name_list)
            sales_list=[i.text for i in self.browser.find_elements_by_css_selector('span[class="sale-num"]')]
            # print(sales_list)
            comment_list=[i.text for i in self.browser.find_elements_by_css_selector('dd[class="rates"] span')]
            # print(comment_list)
            price_list=[i.text for i in self.browser.find_elements_by_css_selector('span[class="c-price"]')]
            # print(price_list)

            self.super_list=[]
            for i in zip(name_list,sales_list,price_list,url_list,comment_list):

                self.super_list.append(i)
            self.insert_mysql()
        for i in range(0,10):
            print('Dealing with ',i,'page')
            get_current_infos()

            element = self.browser.find_element_by_css_selector('a[class="J_SearchAsync next"]')
            actions = ActionChains(self.browser)
            actions.move_to_element(element).perform()
            self.browser.find_element_by_css_selector('a[class="J_SearchAsync next"]').click()
            time.sleep(4)


    def engine_2_save_pics(self):
        self.browser_init()
        self.get_data()
        self.main_img_css='#J_DivItemDesc > p:nth-child(1) > img'
        count=0
        for unit in zip(self.general_url_list,self.general_ID):
            count+=1
            if count<= 14:
                continue
            print('Dealing with nth',count,'url')

            self.browser.get(unit[0])
            self.browser.implicitly_wait(10)
            # self.browser.find_element_by_css_selector('#J_VideoThumb > div > a').click()
            try:
                img_src=self.browser.find_element_by_css_selector(self.main_img_css).get_attribute('src')
            except:
                print('Unable to get pics',count,'nth')
                continue
            print('img_src',img_src)
            with open(f'D:\\taobao\\{unit[1]}.jpg','wb') as imgs:
                img=requests.get(img_src)
                imgs.write(img.content)
                imgs.close()
            time.sleep(3)




if __name__ == '__main__':
    tb=taobao()
    tb.engine_2_save_pics()
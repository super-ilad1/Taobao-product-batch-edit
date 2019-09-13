from selenium import webdriver
import time
import mysql.connector
from selenium.webdriver.common.action_chains import ActionChains
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
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

        self.browser.get('https://item.publish.taobao.com/taobao/manager/render.htm?pagination.current=4&pagination.pageSize=20&spm=a2oq0.12575281.0.d44.25911debz30RIG&tab=in_stock&table.sort.endDate_m=desc')

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

        self.general_infos=[]

        #0-ID 1-name price-3 name_after-6 imgs_index-7 9-product_id
        mycursor.execute("SELECT * FROM blender_plugin where state=1")

        myresult = mycursor.fetchall()

        for i in myresult:
            self.general_infos.append(i)

        print('self.general_infos',self.general_infos)



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

    def next_page(self):
        self.browser.find_element_by_css_selector('#root > div > div > div.next-pagination.next-pagination-normal.next-pagination-medium.medium.ol-next-pagination.list-page-pagination > div > button.next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next').click()
        print('Next page...')
        self.browser.implicitly_wait(5)

    def get_whole_product_link_name_generate_list(self):
        self.link_name_list=[i.text for i in  self.browser.find_elements_by_css_selector('span[class="product-desc-span"] a[target="_blank"]')]
        print('self.link_name_list',self.link_name_list)



    def edit_product_page(self):
        # click edit and entre into new product edit link

        self.browser.find_element_by_css_selector('#root > div > div > div.next-table.only-bottom-border.zebra.manage-o-table.sell-newtable-container > div > div.next-table-body > table > tbody > tr.next-table-row.last.first > td.next-table-cell.last > div > div > div > div > button:nth-child(1)').click()
        self.browser.implicitly_wait(5)

        #skip to newly open edit page
        window_before = self.browser.window_handles[0]

        window_after = self.browser.window_handles[1]
        self.browser.switch_to.window(window_after)

        #turn to title input edit and certificate parameter
        element_ = self.browser.find_element_by_xpath('//*[@id="title"]')
        print('element_.text',element_.get_attribute('value'))
        self.price=0
        self.name_after=''
        self.imgs_index = ''

        for h in self.general_infos:
            if h[1]==element_.get_attribute('value'):
                self.price=str(((float(h[3])+1)/2)-0.1)
                self.name_after=h[6]
                self.name_after=self.name_after.replace(' ','',1)
                self.imgs_index=h[7]
        print('self.name_after',self.name_after,'self.imgs_index',self.imgs_index,'self.price',self.price)

        ActionChains(self.browser).move_to_element(element_).click().perform()
        for i in range(0,70):
            element_.send_keys(Keys.BACKSPACE)
        element_.send_keys(self.name_after)


        # move to price edit input
        element = self.browser.find_element_by_css_selector('#price')
        ActionChains(self.browser).move_to_element(element).click().perform()

        for i in range(0,6):
            element.send_keys(Keys.BACKSPACE)

        element.send_keys(self.price)


        # move to main img edit
        ActionChains(self.browser).move_to_element(self.browser.find_element_by_css_selector('#struct-descType > div > div.next-col.next-col-4 > label')).perform()
        main_img_xpath=    '//*[@id="struct-images"]/div/div[2]/div[1]/div[2]/div/div/div/div[1]/p'
        ActionChains(self.browser).move_to_element(WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, main_img_xpath)))).perform()

        # click delete imgs
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                    "#struct-images > div > div.next-col.next-col-20.sell-o-addon-content > div.sell-o-addon-info > div.info-content > div > div > div > div:nth-child(1) > div.sell-o-image-item-preview > div.image-tools > i.next-icon.next-icon-ashbin.next-icon-small.tool.image-upload-remove"))).click()

        # click add new img
        self.browser.find_element_by_css_selector(
            '#struct-images > div > div.next-col.next-col-20.sell-o-addon-content > div.sell-o-addon-info > div.info-content > div > div > div > div:nth-child(1) > div.image-upload-btn > div > i').click()


        # click img search input
        # time.sleep(1)
        # try:
        #     iframe=WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div:nth-child(33) > div > div > div > div > iframe')))
        #     self.browser.switch_to.frame(iframe)
        # except:
        self.browser.switch_to.frame(1)

        img_search_css = '#container > div > div.hasEms.container > div.main > div > div.opt-body > div.list > div.search-bar > div:nth-child(3) > span.next-input.next-input-single.next-input-medium.clear > input[type=text]'
        search_element=WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, img_search_css)))


        search_element.click()
        search_element.send_keys(self.imgs_index)
        search_element.send_keys(Keys.ENTER)


        time.sleep(1)
        # click first target img
        self.browser.find_element_by_css_selector('#items > div > div.cover.list-item > img').click()

        self.browser.switch_to.default_content()


        #save draft
        ActionChains(self.browser).move_to_element(self.browser.find_element_by_css_selector('#struct-shopcat > div > div.next-col.next-col-4 > label')).perform()

        self.browser.find_element_by_css_selector('#button-submit').click()
        time.sleep(2)
        #close current website
        self.browser.close()
        self.browser.switch_to.window(window_before)


    def update_adjusted(self):


        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            database="taobao"
        )

        mycursor = mydb.cursor()
        #2 represents updated
        sql='update blender_plugin set state=2 where product_id=(%s) '
        val=(self.id,)
        mycursor.execute(sql,val)
        mydb.commit()
        print('update success to state 2')

    def engine_adjust_product(self):


        '''-----------------------------------------------'''
        def input_id(content):
            #re-set
            self.browser.find_element_by_css_selector('#root > div > div > div.manage-container-filter > div.filter-footer > button:nth-child(2)').click()

            #inputing
            input=self.browser.find_element_by_css_selector('#root > div > div > div.manage-container-filter > div.manage-catlist.filter-catlist-container > div > div.queryItemId-sell-hoc.sell-hoc-row.cat-sub-items > div.sellhoc-container-col > div > div > span > span > span > input[type=text]')
            input.send_keys(content)

            #click search
            time.sleep(1)
            self.browser.find_element_by_css_selector('#root > div > div > div.manage-container-filter > div.filter-footer > button:nth-child(1)').click()


        '''-----------------------------------------------'''

        self.browser_init()
        self.get_data()

        for i in self.general_infos:
            self.id=i[9]
            input_id(self.id)


            self.edit_product_page()
            self.update_adjusted()









    def engine_scrape_product_id(self):

        def update_id(id,name):
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                database="taobao"
            )

            mycursor = mydb.cursor()
            sql='update blender_plugin set product_id=(%s) where name=(%s)'
            val=(id,name)
            mycursor.execute(sql,val)
            mydb.commit()
            print('update....',id,name)

        def get_mysql_name():

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                database="taobao"
            )

            mycursor = mydb.cursor()
            name_super_list = []
            mycursor.execute('select name from blender_plugin')
            for i in mycursor.fetchall():
                name_super_list.append(i[0])
            print(name_super_list)
            return name_super_list

        self.browser_init()
        name_list=get_mysql_name()

        #move to first page
        ActionChains(self.browser).move_to_element(self.browser.find_element_by_css_selector('#root > div > div > div.next-pagination.next-pagination-normal.next-pagination-medium.medium.ol-next-pagination.list-page-pagination > div > div.next-pagination-jump > span.next-input.next-input-single.next-input-medium > input[type=text]')).click().send_keys('1').perform()
        self.browser.find_element_by_css_selector('#root > div > div > div.next-pagination.next-pagination-normal.next-pagination-medium.medium.ol-next-pagination.list-page-pagination > div > div.next-pagination-jump > button').click()

        self.browser.refresh()




        for h in range(1,10):


            self.id_list=[]
            for i in self.browser.find_elements_by_css_selector('span[class="product-desc-span"] a'):
                href=i.get_attribute('href')

                href=href.split('id=',1)[1]
                print('href-',href)
                self.id_list.append(href)


            self.name_list=[i.text for i in self.browser.find_elements_by_css_selector('span[class="product-desc-span"] a')]

            print('self.id_list',self.id_list)
            print('self.name_list',self.name_list)

            for i in zip(self.id_list,self.name_list):
                if i[1] in name_list:
                    update_id(i[0],i[1])
                else:
                    print(i[1],'unmatch name to id')

            self.next_page()
            self.browser.refresh()


if __name__ == '__main__':
    tb=taobao()
    tb.engine_adjust_product()

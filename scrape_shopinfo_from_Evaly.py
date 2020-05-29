from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import sqlite3

driver = webdriver.Chrome("chromedriver.exe")
#setting options to open incognito window
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=chrome_options)



def load_page(url='https://www.google.com',error_element='//div[@class="error-code"]'):
    """"Tries to load the URL. If it finds error element by XPATH then it reloads the page.\nIf it doesn't finds the error element then it returns form the function.\n
    Requited imports\n
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    """
    driver.get(url)
    while True:
        try:
            WebDriverWait(driver, .1).until(EC.presence_of_element_located((By.XPATH, error_element)))
        except TimeoutException:
            return
        driver.refresh()


#function to load elements
def load_elements(css_selector=".buy-button",page_ups=1,wait_max=20,time_to_wait=1):
    """
    Loads elements of by CSS class selector\nWaits for 20 seconds to load new items.\nCustomizable if needed.\n\nRequited imports\n
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from time import sleep\n
    """
    old_elements_count = None
    new_elements_count = 0
    while new_elements_count != old_elements_count:
        old_elements_count = new_elements_count #replacing old button count
        new_elements_count = len(driver.find_elements_by_css_selector(css_selector)) #getting new button count

        count = 0
        if old_elements_count==new_elements_count:
            for i in range(wait_max):
                new_elements_count = len(driver.find_elements_by_css_selector(css_selector)) #getting new button count
                if not new_elements_count == old_elements_count:
                    count +=1
                    break
                if i==2:
                    for i in range(page_ups):
                        driver.find_element_by_tag_name('html').send_keys(Keys.PAGE_UP)
                    sleep(time_to_wait*2)
                sleep(time_to_wait*.5) #waits for .7 secs
        if count == wait_max:
            break
        
        #scrolling down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("found new",new_elements_count-old_elements_count,"elements")
        sleep(time_to_wait)

    return new_elements_count


load_page("https://evaly.com.bd/express/express-grocery")

html = driver.find_element_by_tag_name('html')
html.send_keys(Keys.PAGE_DOWN)


#scrolling down to load shops
shops_selector = ".w-full.cursor-pointer.h-full"#"cursor-pointer h-full"
print(f'There is {load_elements(shops_selector,2)} shops in the page')
#selecting loaded shops
shops = driver.find_elements_by_xpath("//a[@class='w-full cursor-pointer h-full']")
shops={shop.text.replace(',','').replace('\'','').replace('’','').replace('"','').replace('(','').replace(')','').replace('.','').replace(' ','_').replace('-','_').replace('/','_').replace('+','_').replace('&','_').replace('__','_'):shop.get_attribute("href") for shop in shops}



connection = sqlite3.connect('evaly.db') #if 'name.db' exists then connect to it else create 'name.db' and connect to it
db_cursor = connection.cursor() #creating cursor to execute sql commands
db_cursor.execute("CREATE TABLE Express_Shops_Details (shop_number INT, shop_name TEXT, phone TEXT, location TEXT, web_address TEXT);")
insert_query = "INSERT INTO Express_Shops_Details VALUES(?,?,?,?,?);"

shop_count=1
total_shops = len(shops.keys())
for shop_name,shop_link in shops.items():
    
    load_page(shop_link)
    print(f'\nworking on shop no {shop_count} out of {total_shops}\n')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[3]/div/div[1]/div[2]/div[2]/div[2]/a')))
    shop_location = driver.find_element_by_xpath('//*[@id="__next"]/div/div[3]/div/div[1]/div[2]/div[2]/div[1]/p').text
    shop_phone_no = driver.find_element_by_xpath('//*[@id="__next"]/div/div[3]/div/div[1]/div[2]/div[2]/div[2]/a').text

    data = (shop_count, shop_name, shop_phone_no, shop_location, shop_link)
    db_cursor.execute(insert_query,data)
    shop_count+=1


driver.quit()

connection.commit() #commiting changes to the database
connection.close() #closing the connection
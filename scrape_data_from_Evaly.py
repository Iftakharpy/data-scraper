from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://evaly.com.bd/express/express-grocery")
driver.maximize_window()

#function to load elements
def load_elements(selector=".buy-button",wait_max=20):
    """Load elements of by CSS class selector\nWaits for 20 seconds to load new items.\nCustomizable if needed."""
    old_elements_count = None
    new_elements_count = 0
    while new_elements_count != old_elements_count:
        old_elements_count = new_elements_count #replacing old button count
        new_elements_count = len(driver.find_elements_by_css_selector(selector)) #getting new button count

        count = 0
        if old_elements_count==new_elements_count:
            for i in range(wait_max):
                new_elements_count = len(driver.find_elements_by_css_selector(selector)) #getting new button count
                if not new_elements_count == old_elements_count:
                    count +=1
                    break
                driver.find_element_by_tag_name('html').send_keys(Keys.PAGE_UP)
                sleep(.4)
                driver.find_element_by_tag_name('html').send_keys(Keys.PAGE_UP)
                sleep(1)
        if count == wait_max:
            break
        
        #scrolling down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("found new",new_elements_count-old_elements_count,"buttons")
        sleep(.5)
    return new_elements_count




html = driver.find_element_by_tag_name('html')
html.send_keys(Keys.PAGE_DOWN)


#scrolling down to load shops
shops_selector = ".w-full.cursor-pointer.h-full"#"cursor-pointer h-full"
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, shops_selector)))
print(f'There is {load_elements(shops_selector)} shops in the page')
#selecting loaded shops
shops = driver.find_elements_by_xpath("//a[@class='w-full cursor-pointer h-full']")

#closing the browser
driver.quit()


import sqlite3

connection = sqlite3.connect('Products_in_shops_from_Evaly.db') #if test.db exists then connect to it else create test.db and connect to it
print(connection)
print('creating cursor on sqlite3')
db_cursor = connection.cursor() #creating cursor to execute sql commands
print(db_cursor)
for shop in shops:
    #opening browser and going to shop link
    driver.get(str(shop.get_attribute('href')))
    driver.maximize_window()


    shop_name = shop.text.replace(' ','_')
    #creating TABLE using shop_name
    print(f'cleating table {shop_name}')
    create_table = f"CREATE TABLE {shop_name} (product_number INT, product_name  TEXT, price_with_taka_symbol TEXT, price INT);"
    db_cursor.execute(create_table)



    #scrolling down to load buy-buttons
    print(f'There is {load_elements()} buttons in the page')

    #scrolling to get to the top of the page 
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.HOME)
    html.send_keys(Keys.PAGE_DOWN)

    product_titles = driver.find_elements_by_xpath('//p[@class="ShopProductCard___StyledP-cujg6o-1 eJXTjd font-semibold md:text-base text-sm text-center"]')
    print(f'found {len(product_titles)} titles')
    product_prices = driver.find_elements_by_xpath("//span[@class='text-lg font-semibold px-2']")
    print(f'found {len(product_prices)} prices')
    driver.quit()
    
    print(f'inserting data into {shop_name} table')
    insert_query = f"INSERT INTO {shop_name} VALUES(?,?,?,?);"
    for i in range(len(product_prices)):
        print(f"INSERT INTO {shop_name} VALUES({i+1},{product_titles[i]},{product_prices[i]},{product_prices[i][1:]})")
        data = (i+1,product_titles[i],product_prices[i].text,product_prices[i].text[1:])
        db_cursor.execute(insert_query,data)


connection.commit() #commiting changes to the database
connection.close() #closing the connection
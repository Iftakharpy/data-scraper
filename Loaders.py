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


# Function to load webpage if it doesn't response in the first try.
# Or if the network diconnects it will keep reloading the page until network is connected and page is loaded.  
def load_page(url='https://www.google.com',error_element='//div[@class="error-code"]'):
    """"Tries to load the URL. If it finds error element by XPATH then it reloads the page.\nIf it doesn't finds the error element then it returns form the function.\n
    Requited imports:\n
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


#Function to load elements in a dynamically loading page
def load_elements(css_selector=".buy-button",page_ups=1,wait_max=20,time_to_wait=1):
    """
    Loads elements of a page by CSS class selector\nWaits for 20 seconds to load new items.\nCustomizable if needed.\n\n
    Requited imports:\n
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
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import pandas as pd
import time

#Creating chrome driver to be used with selenium 
chrome_options=Options() 
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=chrome_options))


#Getting the target website
website="https://www.ebay.com/b/Cell-Phones-Smartphones/9355/bn_320094?_pgn=1&rt=nc"
driver.get(website)
time.sleep(5)
driver.maximize_window()

# using stealth to masking the scraping process
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
)
time.sleep(3)

#creating all needed lists
titles=[]
prices=[]
status=[]
views=[]
images_links=[]


#Pagination
nav_bar=driver.find_element(By.XPATH,'//nav[@class="pagination"]')
pages=nav_bar.find_elements(By.XPATH,'./ol[@class="pagination__items"]/li')

last_page=5

current_page=1

#starting the scraping
while current_page<=last_page:
    time.sleep(10)
    try:
        container=driver.find_element(By.XPATH,'//section[@class="brw-river bwrvr"]/ul')
        boxes=container.find_elements(By.XPATH,'./li')

        for box in boxes:

            try:
                title=box.find_element(By.XPATH,'.//h3[contains(@class,"__title__text")]').text
                titles.append(title)
                prices.append(box.find_element(By.XPATH,'.//span[@class="textual-display bsig__price bsig__price--displayprice"]').text)
                status.append(box.find_element(By.XPATH,'.//span[@class="textual-display bsig__generic bsig__listingCondition"]').text)
                try:
                    views.append(box.find_element(By.XPATH,'.//span[contains(@class,"ric bsig____search.watchCountTotal")]').text)
                except:
                    views.append("No Views")
                try:
                    image_element=box.find_element(By.TAG_NAME,"img")
                    images_links.append(image_element.get_attribute("data-src"))


                except:
                    print(f"this box {title} has no image ")
            
            except:
                print(f"couldn't scrape this phone{box.text}")
    except:
        print(f"there is a problem in page {current_page}")
    
    #navigation to next page
    try:

        if current_page<last_page:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            next_page=driver.find_element(By.XPATH,'.//a[@type="next" or @aria-label="Go to next page"]')
            next_page.click()
        else:
            print(f"Data Extracted Successfully for the {current_page} pages")
            break
    except:
        
        print(f"there is a problem in navigation to the next page {current_page+1}")
        break # stop the code

    print(current_page)# just for tracking
    current_page+=1


df=pd.DataFrame({"Product Title":titles,"Product Price":prices,"product status":status,"product Views":views,"Product Image":images_links})
df.to_excel(r"C:\Users\hp\Desktop\Python_Web_Scraping\projects\Ebay_Smartphones\Ebay_Smartphones_Data.xlsx", index=False)
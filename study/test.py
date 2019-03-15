#coding:utf-8
from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
'''
import requests
url1 = 'http://bj.58.com/zufang/35068214497737x.shtml'
r1 = requests.get(url1)
cookies = r1.cookies
headers = r1.headers
url = "http://jst1.58.com/counter?infoid=35068214497737&uname=&userid=&totalControl=&listControl=&sid=0&lid=0&px=0&cfpath=&_="+str(int(time.time()*1000))
print url
r = requests.get(url,headers=headers)
print r.content
exit()

'''

driver = webdriver.PhantomJS(executable_path="/Users/NealSu/GoogleDisk/MyTools/Python2.6/Download/phantomjs/bin/phantomjs") 

def wait_for_load(driver):
    try: 
        title = driver.find_element_by_id("totalcount")
    except:
        title = 'None'
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return title
        time.sleep(.5)

        try:
            newtitle = driver.find_element_by_id("totalcount")
        except:
            pass
        if newtitle != title:
            return newtitle


driver.set_page_load_timeout(5)
driver.set_script_timeout(5)
try:
    driver.get("http://bj.58.com/zufang/35068214497737x.shtml")
except:    
    driver.execute_script("window.stop()")
    print driver.find_element_by_id("totalcount").text
try:
    driver.get("http://bj.58.com/zufang/35068214497737x.shtml")
except:    
    driver.execute_script("window.stop()")
    print driver.find_element_by_id("totalcount").text
try:
    driver.get("http://bj.58.com/zufang/35068214497737x.shtml")
except:    
    driver.execute_script("window.stop()")
    print driver.find_element_by_id("totalcount").text
#print wait_for_load(driver).text
#print (driver.page_source)
driver.quit()

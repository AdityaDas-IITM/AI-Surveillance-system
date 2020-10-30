from selenium import webdriver
import time
import os
from selenium.webdriver.common.keys import Keys

def send_vid(driver, phone, path): 
    
    # type and send the msg
    inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
    input_box = driver.find_element_by_xpath(inp_xpath)
    input_box.send_keys('Alert' + Keys.ENTER)

    # attachment button click
    driver.find_element_by_css_selector("span[data-icon='clip']").click()
    time.sleep(1)

    # add file to send by file path
    driver.find_element_by_css_selector("input[type='file']").send_keys(path)
    time.sleep(3)

    # click to send
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div").click()
    time.sleep(1)

if __name__ == '__main__':
    
    driver = webdriver.Chrome(executable_path='../scripts/chromedriver.exe')
    wapp = "https://web.whatsapp.com"
    driver.get(wapp)
    time.sleep(15)
    path = os.getcwd().replace(os.sep, '/') + "/app_uploaded_files/output.mp4"
    send_vid(driver, "+919740718396", path)
    '''
    url = 'https://web.whatsapp.com/send?phone='+'+919591260537'
    driver = webdriver.Chrome(executable_path='../scripts/chromedriver.exe')
    driver.get(url)
    time.sleep(15)
    inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
    for i in range(5):
        input_box = driver.find_element_by_xpath(inp_xpath)
        input_box.send_keys('Alert' + Keys.ENTER)
    '''
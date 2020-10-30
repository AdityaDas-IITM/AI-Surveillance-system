from selenium import webdriver
import time
import os

def send_vid(driver, phone, path): 
    url = 'https://web.whatsapp.com/send?phone='+phone+'&text='+'Alert'
    # load the person's chat
    driver.get(url)
    time.sleep(5)

    # send test message Nigal
    driver.find_element_by_css_selector("span[data-icon='send']").click()
    time.sleep(0.5)

    # attachment button click
    driver.find_element_by_css_selector("span[data-icon='clip']").click()
    time.sleep(1)

    # add file to send by file path
    driver.find_element_by_css_selector("input[type='file']").send_keys(path)
    time.sleep(2)

    # click to send
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div").click()
    time.sleep(5)

if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path='../scripts/chromedriver.exe')
    wapp = "https://web.whatsapp.com"
    driver.get(wapp)
    time.sleep(15)
    path = os.getcwd().replace(os.sep, '/') + "/app_uploaded_files/output.mp4"
    send_vid(driver, "+919740718396", path)

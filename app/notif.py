from selenium import webdriver
import time

def send_vid(driver, phone, path): 
    url = 'https://web.whatsapp.com/send?phone='+phone+'&text='+'Alert'
    # load the person's chat
    driver.get(url)
    time.sleep(10)

    # send test message Nigal
    driver.find_element_by_css_selector("span[data-icon='send']").click()
    time.sleep(5)

    # attachment button click
    driver.find_element_by_css_selector("span[data-icon='clip']").click()
    time.sleep(5)

    # add file to send by file path
    driver.find_element_by_css_selector("input[type='file']").send_keys(path)
    time.sleep(5)

    # click to send
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div").click()
    time.sleep(5)

if __name__ == '__main__':
    '''
    phone = "+919740718396"
    message = 'Nigal'

    wapp = "https://web.whatsapp.com"
    url1 = 'https://web.whatsapp.com/send?phone='+phone+'&text='+message
    url2 = 'https://web.whatsapp.com/send?phone=+918105632052&text=nibbi'

    driver = webdriver.Chrome(executable_path='/scripts/chromedriver.exe')

# load web whatsapp main page
    driver.get(wapp) 
    time.sleep(15)
    send_vid(url1)  # joy
    send_vid(url2)  # pandey
    '''
    driver = webdriver.Chrome(executable_path='../scripts/chromedriver.exe')
    wapp = "https://web.whatsapp.com"
    driver.get(wapp)
    time.sleep(15)
    path = "D:/Github Repos/AI-Surveillance-system/app_uploaded_files/output.mp4"
    send_vid(driver, "+919740718396", path)

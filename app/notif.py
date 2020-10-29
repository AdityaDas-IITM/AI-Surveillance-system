from selenium import webdriver
import time

def send_vid(phone):

    wapp = "https://web.whatsapp.com"
    url = 'https://web.whatsapp.com/send?phone='+phone+'&text='+'Alert'
    driver.get(wapp) 
    # load the person's chat
    driver.get(url)
    time.sleep(0.1)

    # send test message Nigal
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]/button").click()
    time.sleep(0.1)

    # attachment button click
    driver.find_element_by_css_selector("span[data-icon='clip']").click()
    time.sleep(0.1)
    # add file to send by file path
    driver.find_element_by_css_selector("input[type='file']").send_keys("D:/Github Repos/AI-Surveillance-system/app_uploaded_files/output.mp4")
    time.sleep(0.1)
    # click to send
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div").click()

if __name__ == '__main__':
    phone = "+919740718396"
    message = 'Nigal'

    wapp = "https://web.whatsapp.com"
    url1 = 'https://web.whatsapp.com/send?phone='+phone+'&text='+message
    url2 = 'https://web.whatsapp.com/send?phone=+918105632052&text=nibbi'

    driver = webdriver.Chrome(executable_path='C:/Users/nihal/Downloads/chromedriver.exe')

# load web whatsapp main page
    driver.get(wapp) 
    time.sleep(15)
    send_vid(url1)  # joy
    send_vid(url2)  # pandey

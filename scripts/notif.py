from selenium import webdriver
import time

joy_phone = "+919740718396"
joy_message = 'Nigal'

pand_phone = "+918105632052"
pand_message = 'nibbi'

vid_path = "C:/Users/nihal/Pictures/Camera Roll/hand_track_output.mp4"

wapp = "https://web.whatsapp.com"

driver = webdriver.Chrome(executable_path='C:/Users/nihal/Downloads/chromedriver.exe')

# load web whatsapp main page
driver.get(wapp) 
time.sleep(15)

def send_vid(phone, message, file=''):
    url = 'https://web.whatsapp.com/send?phone='+phone+'&text='+message
    # load the person's chat
    driver.get(url)
    time.sleep(5)

    # send test message Nigal
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]/button").click()
    time.sleep(2)

    if file != '':
        # attachment button click
        driver.find_element_by_css_selector("span[data-icon='clip']").click()
        time.sleep(2)
        # add file to send by file path
        driver.find_element_by_css_selector("input[type='file']").send_keys("C:/Users/nihal/Pictures/Camera Roll/hand_track_output.mp4")
        time.sleep(2)
        # click to send
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div").click()
        time.sleep(10)

send_vid(joy_phone, joy_message, vid_path)  # joy
send_vid(pand_phone, pand_message, vid_path)  # pandey

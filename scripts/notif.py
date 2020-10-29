from selenium import webdriver
import time

<<<<<<< HEAD

=======
joy_phone = "+919740718396"
joy_message = 'Nigal'

pand_phone = "+918105632052"
pand_message = 'nibbi'

vid_path = "C:/Users/nihal/Pictures/Camera Roll/hand_track_output.mp4"

wapp = "https://web.whatsapp.com"
>>>>>>> 2cc930391f5ea32a28d8aa27f5a2a2c66432dd5e

def send_vid(url, phone):

<<<<<<< HEAD
    wapp = "https://web.whatsapp.com"
    url1 = 'https://web.whatsapp.com/send?phone='+phone+'&text='+'Alert'
    driver.get(wapp) 
=======
# load web whatsapp main page
driver.get(wapp) 
time.sleep(15)

def send_vid(phone, message, file=''):
    url = 'https://web.whatsapp.com/send?phone='+phone+'&text='+message
>>>>>>> 2cc930391f5ea32a28d8aa27f5a2a2c66432dd5e
    # load the person's chat
    driver.get(url)
    time.sleep(5)

    # send test message Nigal
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]/button").click()
    time.sleep(0.1)

<<<<<<< HEAD
    # attachment button click
    driver.find_element_by_css_selector("span[data-icon='clip']").click()
    time.sleep(0.1)
    # add file to send by file path
    driver.find_element_by_css_selector("input[type='file']").send_keys("C:/Users/nihal/Pictures/Camera Roll/hand_track_output.mp4")
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
=======
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
>>>>>>> 2cc930391f5ea32a28d8aa27f5a2a2c66432dd5e

#terminal command: python3 game_handle_ios.py -id 00008020-000D14A03608003A -url https://dev-in-cjb-0.headspin.io:7003/v0/150f14a11db946ffb9505e3175ae9d95/wd/hub
#terminal command: python3 game_handle_ios.py -id 00008020-001E71D10168002E -url https://dev-in-cjb-0.headspin.io:7003/v0/150f14a11db946ffb9505e3175ae9d95/wd/hub
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import argparse
import requests
import imagescraping
from time import sleep
import time
import os


# xpath name
search_icon  = '//XCUIElementTypeStaticText[@label="Search"]'
search_tab = "//XCUIElementTypeSearchField[@name='GMOEIDSearchField']"
seach_icon = "//XCUIElementTypeButton[@name='Google']"
verify_no_net = "//android.widget.TextView[contains(@text,'SIM card not found')]"
game = "(//android.widget.ImageView[@focusable='true'])[2]"

# to get input form the terminal
parser = argparse.ArgumentParser()
parser.add_argument('-id', '--udid', required=True, help='UDID argument description')
parser.add_argument('-url', '--appium_input', required=True, help='Appium Input argument description')
args = parser.parse_args()
udid = args.udid
appium_input = args.appium_input
access_token = appium_input.split('/')[4]

#screenshot
def get_ios_screenshot(filename):
        api_endpoint = "https://api-dev.headspin.io/v0/idevice/{}/screenshot".format(udid)
        r = requests.get(url = api_endpoint,  headers={'Authorization': 'Bearer {}'.format(access_token)})
        print("Status code",r.status_code)
        with open(filename, 'wb') as f:
            f.write(r.content)
            
#creat desired capabilities and driver
desired_caps = {}
desired_caps['platformName'] = "ios"
desired_caps['udid'] = udid
desired_caps['deviceName'] = udid
desired_caps['newCommandTimeout'] = 50000
desired_caps['noReset'] = True
desired_caps['appPackage'] = "com.google.GoogleMobile"
# desired_caps['appActivity'] = 'com.google.android.googlequicksearchbox.SearchActivity'
desired_caps['bundleId'] = "com.google.GoogleMobile"
desired_caps['automationName'] = "XCUITest"
desired_caps['headspin:capture.video'] = True
desired_caps['headspin:capture.network'] = False
driver = webdriver.Remote(
            command_executor=appium_input,
            desired_capabilities=desired_caps
        )
wait = WebDriverWait(driver, 10)
try:
    #open google search app and select the game
    wait.until(EC.presence_of_element_located((MobileBy.XPATH, search_icon))).click()
    assert wait.until(EC.presence_of_element_located((MobileBy.XPATH, search_tab))).is_displayed()
    wait.until(EC.presence_of_element_located((MobileBy.XPATH, search_tab))).send_keys('headpsin')
    # driver.press_keycode(66) # search the entered keyword
    wait.until(EC.presence_of_element_located((MobileBy.XPATH, search_icon))).click()
     
    try:
        assert wait.until(EC.presence_of_element_located((MobileBy.XPATH, verify_no_net))).is_displayed()
        wait.until(EC.presence_of_element_located((MobileBy.XPATH,game))).click()
        
        #play the game
        screen_size = driver.get_window_size()
        center_x = screen_size['width'] // 2
        center_y = screen_size['height'] // 2
        
        for i in range(5):
            for j in range(4):
                action = TouchAction(driver)
                action.tap(x=center_x, y=center_y).perform()
                time.sleep(0.25)
            time.sleep(1)
        
        #take screenshot and extract character
        sleep(5)
        get_ios_screenshot('image.png')
        current_directory = os.getcwd()
        image_path = os.path.join(current_directory, 'image.png')
        imagescraping.extract(image_path)
    except:
        print("game is not displayed.....")
    
finally:
    sleep(5)
    driver.quit()

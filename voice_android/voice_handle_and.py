#package = 'com.google.android.googlequicksearchbox'
#activity = 'com.google.android.googlequicksearchbox.SearchActivity'
# python3 voice_handle_and.py -id RF8M61896NZ -url https://dev-us-sny-1.headspin.io:7039/v0/80baacf2d97e4bd29aa3a361775f0786/wd/hub
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import requests
from time import sleep
import time
import os
from gtts import gTTS
import json
from pydub import AudioSegment


# xpath name
search_icon  = '(//*[@text="Search"])[1]'
search_tab = "//android.widget.EditText[@text = 'Search…']"
voice_btn = '//android.widget.ImageButton[@content-desc="Voice Search"]'
message = "(//android.widget.TextView[@enabled='true'])[1]"

# to get input form the terminal
parser = argparse.ArgumentParser()
parser.add_argument('-id', '--udid', required=True, help='UDID argument description')
parser.add_argument('-url', '--appium_input', required=True, help='Appium Input argument description')
args = parser.parse_args()
udid = args.udid
appium_input = args.appium_input
access_token = appium_input.split('/')[4]

# method to prepare audio
# prepare_audio(access_token,hostname, audio_id)
def prepare_audio(api_key, hostname, audio_ids):
    url = "https://api-dev.headspin.io/v0/audio/prepare"
    data = {
        "hostname": hostname,
        "audio_ids": audio_ids
    }
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        # Make a POST request with the JSON data payload
        response = requests.post(url, headers=headers, json=data)
    except Exception as e:
        # print(f"An error occurred: {str(e)}")
        pass

#method to chech audio is uploaded
def chech_audio_uploaded(api_key,audio_id):
    url = "https://api-dev.headspin.io/v0/audio/list"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    # Make a GET request
    response = requests.get(url, headers=headers)
    r = response.json()
    print("audio id is been uploaded: ",audio_id in r["audio_ids"])

# to get the device adress and device_host
def get_device_address(udid,access_token):
    device_list_url = "https://api-dev.headspin.io/v0/devices"
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    r = requests.get(device_list_url, headers=headers)
    r = r.json()
    devices = r['devices']
    is_desired_device = False
    for device in devices:
        device_os = device['device_type']
        if device_os == "android" and device['serial'] == udid:
                is_desired_device = True
        if is_desired_device:
                device_hostname = device['hostname']
                device_address = "{}@{}".format(
                    udid, device_hostname)
                return device_address,device_hostname
            
# for uploading 
    # curl --request POST https://80baacf2d97e4bd29aa3a361775f0786@api-dev.headspin.io/v0/audio/upload
    #         --data-binary "@/Users/dharnishdp/awf/projectpoc/voice_android/outputwav.wav"
def upload_audio(api_key, audio_file_path):
    url = "https://api-dev.headspin.io/v0/audio/upload"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        with open(audio_file_path, 'rb') as audio_file:
            headers = {
                "Authorization": f"Bearer {api_key}"
            }

            # Make a POST request with data from the file
            response = requests.post(url, headers=headers, data=audio_file)
            r = json.loads(response.text)
            print(r)
            

            if response.status_code == 200:
                print("Audio upload was successful")
                return r['audio_id']
                # You can access the response content with response.text
            else:
                print(f"Audio upload failed with status code {response.status_code}")
                print(response.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# to injected the audio
def start_audio_injection(api_key, device_address, audio_id):
    # API endpoint URL
    url = "https://api-dev.headspin.io/v0/audio/inject/start"
    try:
        # Request data payload
        data = {
            "device_address": device_address,
            "audio_id": audio_id,
            "use_hsp": "true"
        }

        # Set up the request headers with the API key and content type
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json=data)
    except Exception as e:
        pass
           
#creat desired capabilities and driver
desired_caps = {}
desired_caps['platformName'] = "android"
desired_caps['udid'] = udid
desired_caps['deviceName'] = udid
desired_caps['newCommandTimeout'] = 50000
desired_caps['noReset'] = True
desired_caps['appPackage'] = 'com.google.android.googlequicksearchbox'
desired_caps['appActivity'] = 'com.google.android.googlequicksearchbox.SearchActivity'
desired_caps['automationName'] = "UiAutomator2"
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
    sleep(2)
    text = "today weather in india"  # text which is sending
    tts = gTTS(text, lang='en')
    name = "output.mp3"
    tts.save(name)
    
    
    #audio injection
    # os.system("afplay output.mp3") 
    current_directory = os.getcwd()
    mp3_file = os.path.join(current_directory, name)
    audio = AudioSegment.from_mp3(mp3_file)
    namewav = 'outputwav.wav'
    audio.export( namewav, format="wav")
    api_token = access_token
    print(api_token,access_token)
    current_directory = os.getcwd()
    path = os.path.join(current_directory, namewav)
    print(path)
    audio_id = upload_audio(api_token,path) #upload the file
    print(audio_id)
    chech_audio_uploaded(api_token,audio_id)
    device_address,hostname = get_device_address(udid,access_token)
    print(device_address,"  ",hostname)
    prepare_audio(access_token,hostname, [audio_id])
    wait.until(EC.presence_of_element_located((MobileBy.XPATH, voice_btn))).click()
    start_audio_injection(api_token,device_address, audio_id)
    sleep(4)
    
    
    #prove if the text and voice text is maching
    try:
        prove = wait.until(EC.presence_of_element_located((MobileBy.XPATH, message))).text
        print("Test grabed from the search tab: ",prove)
        print("actual text: ",text)
        if prove.lower() == text.lower():
            print("Text is Matching")
        else :
            print("Text is not Matching")
    except:
        print("Not converting the voice commmand to text...")
finally:
    sleep(5)
    driver.quit()
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import requests
from datetime import datetime


def get_rtmp(room_id):
    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}

    driver = webdriver.Chrome(desired_capabilities=caps, executable_path="../util/chromedriver.exe")
    driver.get("https://www.douyu.com/{}".format(room_id))

    performance_data = driver.get_log("performance")
    print(performance_data)

    get_h5_data = None

    for msg in performance_data:
        try:
            data = json.loads(msg['message'])
            if data['message']['params']['request']['url'].__contains__('getH5'):
                #print(data['message']['params']['request']['postData'])
                get_h5_data = data
        except:
            pass

    driver.quit()

    if get_h5_data is None:
        return None

    print(get_h5_data)

    response = requests.post(
        url=get_h5_data['message']['params']['request']['url'],
        data=get_h5_data['message']['params']['request']['postData'],
        headers=get_h5_data['message']['params']['request']['headers']
    )

    print(response)
    print(response.content.decode())

    response = json.loads(response.content.decode())
    if response['error'] != 0:
        return None

    # print(response['data']['rtmp_live'])

    return response['data']['rtmp_url'] + "/" + response['data']['rtmp_live']


def probe_room(room_id):
    response = requests.get("https://www.douyu.com/betard/{}".format(room_id))
    print(response.text)

    room_data = json.loads(response.text)

    print(room_data['room'])

    if room_data['room']['show_status'] == 1:
        return True
    else:
        return False


def download_stream(room_id, path='.'):
    rtmp = get_rtmp(room_id)

    print(rtmp)

    response = requests.get(
        url=rtmp,
        stream='true',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
    )

    if response.status_code != 200:
        print("error when downloading rtmp stream")
        exit()
    else:
        print("ojbk")
        print(response)

    file_name = path
    file_name.replace("\\", "/")
    if file_name[-1] != '/':
        file_name = file_name + '/'
    file_name = file_name + "{}_{}.flv".format(room_id, datetime.timestamp(datetime.now()))
    with open(file_name, 'ab+') as f:
        counter = 0
        for chunk in response.iter_content(chunk_size=102400):
            if chunk:
                counter = counter + 1
                f.write(chunk)
                if counter % 10 == 0:
                    print("chunk:{}M".format(counter / 10))
                f.close()
                f = open(file_name, 'ab+')

if __name__ == '__main__':
    # room_id = 120219
    room_id = 9999

    is_streaming = probe_room(room_id)

    print(str(room_id) + " status : " + str(is_streaming))

    if is_streaming:
        download_stream(room_id, "D:\\")


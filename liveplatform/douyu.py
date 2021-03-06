from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import requests
from datetime import datetime
from liveplatform.live_platform_base import LivePlatformBase
import logging
import config.config


class Douyu(LivePlatformBase):
    def __get_rtmp(self, room_id):

        if config.config.chrome_driver_config["version"] is None:
            driver = webdriver.Chrome(
                executable_path=config.config.chrome_driver_config['executable_path']
            )
            config.config.chrome_driver_config["version"] = driver.capabilities['chrome']['chromedriverVersion']
            logging.info("chromedriver version={}".format(driver.capabilities['chrome']['chromedriverVersion']))
            driver.quit()

        desired_caps = DesiredCapabilities.CHROME
        if int(config.config.chrome_driver_config["version"][0:2]) >= 75:
            desired_caps["goog:loggingPrefs"] = {"performance": "ALL"}
        else:
            desired_caps["loggingPrefs"] = {"performance": "ALL"}

        driver = webdriver.Chrome(
            desired_capabilities=desired_caps,
            executable_path=config.config.chrome_driver_config['executable_path']
        )
        driver.get("https://www.douyu.com/{}".format(room_id))

        performance_data = driver.get_log("performance")
        print(performance_data)

        get_h5_data = None

        for msg in performance_data:
            try:
                data = json.loads(msg['message'])
                if data['message']['params']['request']['url'].__contains__('getH5'):
                    logging.debug("getH5 request data: " + str(data['message']['params']['request']['postData']))
                    get_h5_data = data
            except:
                pass

        driver.quit()

        if get_h5_data is None:
            return None

        logging.debug("getH5 data: " + str(get_h5_data))

        response = requests.post(
            url=get_h5_data['message']['params']['request']['url'],
            data=get_h5_data['message']['params']['request']['postData'],
            headers=get_h5_data['message']['params']['request']['headers']
        )

        response = json.loads(response.content.decode())
        if response['error'] != 0:
            return None

        logging.debug("rtmp live: " + str(response['data']['rtmp_url'] + "/" + response['data']['rtmp_live']))

        return response['data']['rtmp_url'] + "/" + response['data']['rtmp_live']

    def probe_room(self, room_id):
        response = requests.get("https://www.douyu.com/betard/{}".format(room_id))
        room_data = json.loads(response.text)
        if room_data['room']['show_status'] == 1:
            return True
        else:
            return False

    def download_stream(self, room_id, path='.'):
        rtmp = self.__get_rtmp(room_id)
        logging.debug(rtmp)
        response = requests.get(
            url=rtmp,
            stream='true',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
            }
        )

        if response.status_code != 200:
            logging.debug("error when downloading rtmp stream")
            return None
        else:
            logging.debug("download response status code = 200... download start")

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
                    if counter % 100 == 0:
                        logging.info("{} stream download: {}M".format(room_id, counter / 100))
                    f.flush()
                    # f.close()
                    # f = open(file_name, 'ab+')
        return file_name


if __name__ == '__main__':
    room_id = 64609

    douyu = Douyu()

    is_streaming = douyu.probe_room(room_id)

    if is_streaming:
        print("{} is streaming".format(room_id))
        douyu.download_stream(room_id, "D:/qike/")
    else:
        print("{} not streaming".format(room_id))

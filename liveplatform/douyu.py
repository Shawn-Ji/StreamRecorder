from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import requests
from datetime import datetime
from liveplatform.live_platform_base import LivePlatformBase
import logging
import config.config
import util.util as util
import sys


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
        # print(performance_data)

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

    def download_stream(self, room_id, path='.', size_limit=None):
        rtmp = self.__get_rtmp(room_id)
        logging.debug(rtmp)
        file_name = path
        file_name.replace("\\", "/")
        if file_name[-1] != '/':
            file_name = file_name + '/'
        file_name = file_name + "{}_{}.flv".format(room_id, datetime.timestamp(datetime.now()))
        return util.requests_stream_download(
            rtmp,
            file_name,
            size_limit
        )


if __name__ == '__main__':
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(levelname)s]:\t %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)

    room_id = 74960

    douyu = Douyu()

    is_streaming = douyu.probe_room(room_id)

    if is_streaming:
        print("{} is streaming".format(room_id))
        douyu.download_stream(room_id, "D:/test/", 30*1024*1024)
    else:
        print("{} not streaming".format(room_id))

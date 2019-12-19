from liveplatform.live_platform_base import LivePlatformBase
import requests
import json
import logging
from datetime import datetime


class Huya(LivePlatformBase):
    def __get_rtmp(self, room_id):

        r = requests.get(
            url="https://www.huya.com/{}".format(room_id),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
            }
        )
        data = r.content.decode("unicode-escape")
        data = data[data.find("var hyPlayerConfig"):data.find("window.TT_LIVE_TIMING")]
        data = data[data.find("{"):data.rfind("};") + 1]

        data = json.loads(data)

        logging.debug("hyPlayerConfig: " + str(data))
        print("hyPlayerConfig: " + str(data))

        ratio = 0
        for ratio_info in data["stream"]["vMultiStreamInfo"]:
            if ratio_info["iBitRate"] > ratio:
                ratio = ratio_info["iBitRate"]

        print(ratio)

        data = data["stream"]["data"][0]["gameStreamInfoList"]
        game_info_data = data[0]
        logging.debug("gameStreamInfo: " + str(game_info_data))

        url = game_info_data["sFlvUrl"] \
              + "/" + game_info_data["sStreamName"] \
              + ".flv" \
              + "?" + game_info_data["sFlvAntiCode"].replace("&amp;", "&") \
              + "&" + "ratio={}".format(ratio)

        # TODO: parameter: u(dynamic?), sv(static?), t(static?)

        logging.debug("url: " + str(url))
        print(url)
        return url

    def probe_room(self, room_id):
        response = requests.get("https://www.huya.com/{}".format(room_id))
        room_data = response.text
        if room_data.__contains__("liveStatus-off"):
            return False
        else:
            return True

    def download_stream(self, room_id, path='.', size_limit=None):
        rtmp = self.__get_rtmp(room_id)
        logging.debug(rtmp)
        response = requests.get(
            url=rtmp,
            stream='true',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
            }
        )
        print(response)

        if response.status_code != 200:
            #logging.debug("error when downloading rtmp stream")
            return None
        else:
            pass
            # logging.debug("download start")

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
                    f.flush()
                    # f.close()
                    # f = open(file_name, 'ab+')
        return file_name


if __name__ == '__main__':
    room_id = "520888"

    hy = Huya()
    is_streaming = hy.probe_room(room_id)
    if is_streaming:
        print("{} is streaming".format(room_id))
        hy.download_stream(room_id, "D:/")
    else:
        print("{} is not streaming".format(room_id))





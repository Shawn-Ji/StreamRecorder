import logging

chrome_driver_config = {
    "executable_path": "util/chromedriver.exe"
}

task_config = [
    {
        "name": "qike",
        "live_platform_name": "douyu",
        "room_id": "120219",
        "download_path": "D:/qike/",
        # "download_path": "/mnt/pi_extend/stream/qike/",
    },
    {
        "name": "zhou",
        "live_platform_name": "douyu",
        "room_id": "88660",
        "download_path": "D:/zhou/",
        # "download_path": "/mnt/pi_extend/stream/zhou/",
    },
    {
        "name": "xiaojinzhe",
        "live_platform_name": "huya",
        "room_id": "xiaojinzhe",
        "download_path": "D:/xiaojinzhe/",
        # "download_path": "/mnt/pi_extend/stream/xiaojinzhe/",
    }

]

log_config = {
    "file_name": "D:/StreamRecorder.log",
    "file_mode": "a+",
    "level": logging.INFO,
    # "format": "[%(levelname)s]:\t %(message)s - %(asctime)s = %(pathname)s[line:%(lineno)d]",
    "format": "[%(levelname)s]:\t %(message)s",
}

download_status = {


}
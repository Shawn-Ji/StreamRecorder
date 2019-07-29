import logging

chrome_driver_config = {
    "executable_path": "util/chromedriver.exe",
    "version": None
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
        "name": "xiao8",
        "live_platform_name": "douyu",
        "room_id": "64609",
        "download_path": "D:/",
    },
    {
        "name": "zard",
        "live_platform_name": "douyu",
        "room_id": "60937",
        "download_path": "D:/",
    },
    {
        "name": "zsmj",
        "live_platform_name": "douyu",
        "room_id": "52876",
        "download_path": "D:/",
    },
    {
        "name": "sansheng",
        "live_platform_name": "douyu",
        "room_id": "312407",
        "download_path": "D:/",
    },
    # {
    #     "name": "zhou",
    #     "live_platform_name": "douyu",
    #     "room_id": "88660",
    #     "download_path": "D:/zhou/",
    #     # "download_path": "/mnt/pi_extend/stream/zhou/",
    # },
    # {
    #     "name": "xiaojinzhe",
    #     "live_platform_name": "huya",
    #     "room_id": "xiaojinzhe",
    #     "download_path": "D:/xiaojinzhe/",
    #     # "download_path": "/mnt/pi_extend/stream/xiaojinzhe/",
    # }

]

log_config = {
    "file_name": "D:/StreamRecorder.log",
    "file_mode": "a+",
    "level": logging.INFO,
    # "format": "[%(levelname)s]:\t %(message)s - %(asctime)s = %(pathname)s[line:%(lineno)d]",
    "format": "[%(levelname)s]:\t %(message)s",
}

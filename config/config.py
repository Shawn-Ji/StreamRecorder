import logging

task_config = [
    {
        "name": "qike",
        "live_platform_name": "douyu",
        "room_id": "120219",
        "download_path": "D:/qike/"
    },
    {
        "name": "zhou",
        "live_platform_name": "douyu",
        "room_id": "88660",
        "download_path": "D:/zhou/"
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
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import time
import liveplatform.factory
import config.config as config
import logging


def probe_and_download(name, live_platform_name, room_id, download_path, size_limit):
    logging.info("{} job".format(name))

    lp = liveplatform.factory.live_platform_factory(live_platform_name)
    is_streaming = lp.probe_room(room_id)
    if is_streaming:
        logging.info("{} is streaming".format(name))
        lp.download_stream(room_id, download_path, size_limit)
    else:
        logging.info("{} not streaming".format(name))


def task_start():
    logging.basicConfig(
        level=config.log_config['level'],
        filename=config.log_config['file_name'],
        format=config.log_config['format'],
        filemode=config.log_config['file_mode']
    )

    scheduler = BlockingScheduler()

    for task_data in config.task_config:
        scheduler.add_job(
            probe_and_download,
            'interval',
            args=[
                task_data['name'],
                task_data['live_platform_name'],
                task_data['room_id'],
                task_data['download_path'],
                task_data['size_limit']
            ],
            id=task_data['name'],
            minutes=1,
            max_instances=1
        )

        logging.info("add job {}".format(task_data['name']))

    scheduler.start()

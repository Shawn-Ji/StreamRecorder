from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import time
import liveplatform.factory
import config.config as config
import logging


def probe_and_download(name, live_platform_name, room_id, download_path):
    logging.info("{} job".format(name))

    if config.download_status[name] == True:
        logging.info("skip probe {}: downloading status = True".format(name))
        return

    lp = liveplatform.factory.live_platform_factory(live_platform_name)
    is_streaming = lp.probe_room(room_id)
    if is_streaming:
        logging.info("{} is streaming".format(name))
        config.download_status[name] = True
        lp.download_stream(room_id, download_path)
        config.download_status[name] = False
    else:
        logging.info("{} not streaming".format(name))


if __name__ == '__main__':
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
                task_data['download_path']
            ],
            id=task_data['name'],
            minutes=1
        )
        if not config.download_status.__contains__(task_data['name']):
            config.download_status[task_data['name']] = False

        logging.info("add job {}".format(task_data['name']))

    scheduler.start()

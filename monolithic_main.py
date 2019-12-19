import task.task
import logging
import sys

if __name__ == '__main__':
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(levelname)s]:\t %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)

    task.task.probe_and_download(
        "qike",
        "douyu",
        "120219",
        "/video",
        3*1024*1024*1024
    )

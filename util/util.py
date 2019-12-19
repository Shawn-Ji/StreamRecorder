import requests
import logging


def requests_stream_download(url, file_name, size_limit=None):
    response = requests.get(
        url=url,
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

    with open(file_name, 'ab+') as f:
        counter = 0
        for size_counter, chunk in enumerate(response.iter_content(chunk_size=1024*1024)): # 1M chunk
            if chunk:
                f.write(chunk)
                counter += len(chunk)
                if size_counter % 10 == 0:
                    logging.info("stream download: {}B".format(counter))
                f.flush()
                if size_limit is not None and counter > size_limit:
                    f.close()
                    logging.info("file size reached {} Byte, stop record".format(size_limit))
                    response.close()
                    break
            else:
                logging.info("download finished")

from requests.exceptions import ConnectionError, HTTPError, Timeout, RequestException

import logging
import os
import requests


if not os.path.exists("/script/logs"):
    os.makedirs("/script/logs")

log_format = "%(asctime)s - %(name)s:%(levelname)s - %(message)s"
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

file_handler = logging.FileHandler("/script/logs/Download.log", mode="w")
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def download_file(url: str) -> None:
    """
    Download all required input data from IEEE

    :param str url: URL of the file to be downloaded
    :return: None
    """

    try:
        get_response = requests.get(url, stream=True)
        get_response.raise_for_status()

        file_name = url.split("/")[-1]
        with open("/script/input_data/" + file_name, "wb") as f:
            for chunk in get_response.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)

    except (ConnectionError, HTTPError, Timeout, RequestException) as exception:
        logger.error(
            f"Unable to download file!\nURL:{url}\nError message was:\n{exception}"
        )
        raise SystemExit(1)
    except OSError as exception:
        logger.error(f"OS module error!\nError message was:\n{exception}")
        raise SystemExit(1)


if __name__ == "__main__":
    download_file("http://standards-oui.ieee.org/oui/oui.csv")

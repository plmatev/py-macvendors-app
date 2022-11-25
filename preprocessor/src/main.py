from concurrent.futures.thread import ThreadPoolExecutor
from download_input_data import download_file

from parse import parse_data


IANA_BLOCK_MAL = "http://standards-oui.ieee.org/oui/oui.csv"
IANA_BLOCK_MAM = "http://standards-oui.ieee.org/oui28/mam.csv"
IANA_BLOCK_MAS = "http://standards-oui.ieee.org/oui36/oui36.csv"


def main() -> None:
    """
    Main function will invoke helper functions to download input files, parse them and write output to MongoDB

    :return: None
    """

    for url in (IANA_BLOCK_MAL, IANA_BLOCK_MAM, IANA_BLOCK_MAS):
        download_file(url)

    with ThreadPoolExecutor(max_workers=3) as t_pool:
        for url in (IANA_BLOCK_MAL, IANA_BLOCK_MAM, IANA_BLOCK_MAS):
            file_name = url.split("/")[-1]
            t_pool.submit(parse_data, file_name)


if __name__ == '__main__':
    main()

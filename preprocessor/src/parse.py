from dotenv import load_dotenv
from pymongo import ASCENDING, IndexModel, MongoClient
from pymongo.errors import DuplicateKeyError, ExecutionTimeout, OperationFailure, NetworkTimeout, ServerSelectionTimeoutError

import csv
import logging
import os


load_dotenv()

mongo_user = os.getenv("mongo_user")
mongo_pass = os.getenv("mongo_pass")

if not os.path.exists("/script/logs"):
    os.makedirs("/script/logs")

log_format = '%(asctime)s - %(name)s:%(levelname)s - %(message)s'
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

file_handler = logging.FileHandler("/script/logs/Mongo.log", mode='w')
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

DB_COL_NAME = {
    "mam": "MA_M",
    "oui36": "MA_S",
    "oui": "MA_L",
}


def parse_data(file: str) -> None:
    """
    Process and parse the file in scope and will calculate MAC address ranges

    :param str file: relative path to the file, subject of processing
    :return: None
    """

    with open("/script/input_data/" + file, encoding='utf-8', newline='') as f:
        mongo_client = MongoClient(f"mongodb://{mongo_user}:{mongo_pass}@mongodb:27017/")
        mongo_db = mongo_client["MacAddrRange"]

        try:
            mongo_collection_name = DB_COL_NAME[file.split(".")[0]]
        except KeyError as exception:
            logger.error(f'Unknown input filename!\nError message was:\n{exception}')
            raise SystemExit(1)

        try:
            collections = mongo_db.list_collection_names()
        except (OperationFailure, NetworkTimeout, ServerSelectionTimeoutError) as exception:
            logger.error(f'Failed to get MongoDB collections!\nError message was:\n{exception}')
            raise SystemExit(1)

        if mongo_collection_name not in collections:
            compound_idx_mac_b10_lh = IndexModel(
                [
                    ("mac_b10_l", ASCENDING),
                    ("mac_b10_h", ASCENDING)
                ],
                name="mac_b10_l_ASC_mac_b10_h_ASC"
            )

            compound_idx_mac_b10_hl = IndexModel(
                [
                    ("mac_b10_h", ASCENDING),
                    ("mac_b10_l", ASCENDING)
                ],
                name="mac_b10_h_ASC_mac_b10_l_ASC"
            )

            unique_idx_mac_prfx = IndexModel(
                [
                    ("mac_b16_oui", ASCENDING)
                ],
                name="mac_b16_prefix_ASC",
                unique=True
            )

            mongo_db[mongo_collection_name].create_indexes(
                [
                    compound_idx_mac_b10_lh,
                    compound_idx_mac_b10_hl,
                    unique_idx_mac_prfx
                ]
            )

        mongo_collection = mongo_db[mongo_collection_name]

        r = csv.reader(f, delimiter=',')
        next(r)  # Skip the first row of csv file (ignore column header/title)
        for i, row in enumerate(r):
            mac_raw = row[1].strip()
            mac_start = mac_raw.ljust(12, "0")
            mac_end = mac_raw.ljust(12, "F")
            mac_start_int = int(mac_start, 16)
            mac_end_int = int(mac_end, 16)

            try:
                mongo_collection.update_one(
                    {
                        "mac_b16_oui": mac_raw
                    },
                    {
                        "$set":
                            {
                                "company": row[2].strip(),
                                "address": row[3].strip(),
                                "mac_b16_oui": mac_raw,
                                "mac_b16_l": mac_start,
                                "mac_b16_h": mac_end,
                                "mac_b10_l": mac_start_int,
                                "mac_b10_h": mac_end_int,
                                "alloc_block": row[0],
                            }
                    },
                    upsert=True,
                )

            except (DuplicateKeyError, ExecutionTimeout, OperationFailure) as exception:
                logger.warning(f'Failed to update MongoDB document!\nError message was:\n{exception}')

        mongo_client.close()


if __name__ == '__main__':
    parse_data("oui36.csv")

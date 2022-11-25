def mac_block_helper(mac_block_db_doc: dict) -> dict:
    """
    Process and parse returned MongoDB document and return transformed dict

    :param dict mac_block_db_doc: MongoDB document object
    :return: dict
    """

    mac_prefix_sep = ':'.join(mac_block_db_doc["mac_b16_oui"][i:i + 2]
                              for i in range(0, len(mac_block_db_doc["mac_b16_oui"]), 2)
                              )

    return {
        "result":
            {
                "company": mac_block_db_doc["company"],
                "mac_prefix": mac_prefix_sep,
                "address": mac_block_db_doc["address"],
                "start_hex": mac_block_db_doc["mac_b16_l"],
                "end_hex": mac_block_db_doc["mac_b16_h"],
                "country": None,
                "type": mac_block_db_doc["alloc_block"]
            }
    }


def company_block_helper(mac_block_db_doc: dict) -> dict:
    """
    Process and parse returned MongoDB documents and return transformed dict

    :param dict mac_block_db_doc: MongoDB document object
    :return: dict
    """

    return {
            "company": mac_block_db_doc["company"],
            "start_hex": mac_block_db_doc["mac_b16_l"],
            "end_hex": mac_block_db_doc["mac_b16_h"],
    }

from typing import Tuple

import re


MAC_F_COLON = {"regex": re.compile(r"^[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}$"), "sep": ":"}
MAC_F_HYPHEN = {
    "regex": re.compile(r"^[0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5}$"),
    "sep": "-",
}
MAC_F_DOT = {"regex": re.compile(r"^[0-9a-fA-F]{4}(\.[0-9a-fA-F]{4}){2}$"), "sep": "."}
MAC_F_STR = {"regex": re.compile(r"^[0-9a-fA-F]{12}$"), "sep": ""}


def mac_to_int(mac_address: str) -> Tuple[str, int]:
    """
    Search for regex pattern and if there is match, calculate and return base-10 representation of input MAC address.
    Else return empty strings.

    :param str mac_address: MAC address with either no separator or separated by: ":" or "-" or "."(Cisco-like)
    :return: tuple
    """

    mac_raw, mac_int = "", ""

    for re_pattern, separator in (
        MAC_F_COLON.values(),
        MAC_F_HYPHEN.values(),
        MAC_F_DOT.values(),
        MAC_F_STR.values(),
    ):

        try:
            mac_raw = re.search(re_pattern, mac_address.strip()).group()
            mac_int = int(mac_raw.replace(separator, ""), 16)
        except AttributeError:
            continue

    return mac_raw, mac_int

# Description: std library
# Author: Kireev Georgiy <metallerok@gmail.com>
# Copyright (C) 2018 by Kireev Georgiy

import sys
import datetime
from uuid import UUID


def std_debug(param, need_exit=True):
    """
    print param value on console and stop
    executing script if it need
    :param param:
    :param need_exit: boolean, optional
    :return: void
    """
    now = datetime.datetime.now()
    print(now.strftime("%d-%m-%Y %H:%M"), " >> ", param)
    if need_exit:
        sys.exit()


def byte_size(string):
    """
    return byte size of string
    :param string: str
    :return: int
    """
    return len(string.encode('utf-8'))


def is_lower_case(str):
    return str == str.lower()


def is_upper_case(str):
    return str == str.upper()


def capitalize(string, lower_rest=False):
    """
    capitalize first letter in string
    :param string: str
    :param lower_rest: bool
    :return: str
    """
    return string[:1].upper() + (string[1:].lower() if lower_rest else string[1:])


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

    Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

    Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.
    """

    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except:
        return False

    return str(uuid_obj) == uuid_to_test

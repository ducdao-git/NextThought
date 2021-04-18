import json
from urllib import request, error

from libs.backend.custom_exception import DataError


def is_internet_connected():
    try:
        request.urlopen('https://www.google.com/', timeout=3)
        return True

    except error.URLError:
        return False


def get_response_data(response):
    """
    get the data of a request or raise exception if request is bad
    :param response: a request obj
    :return: response data of the request or None if exception raise
    """
    if response.status_code == 200:
        content = json.loads(response.content)
        return content

    elif response.status_code == 400:  # API rejects action
        message = json.loads(response.content)['message']
        raise DataError(message)

    else:
        raise DataError({'status code': response.status_code})

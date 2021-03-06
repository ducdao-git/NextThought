import json

from libs.backend.custom_exception import DataError


def get_response_data(response):
    """
    get the data of a request or raise exception if request is bad
    :param response: a request obj repr a response
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

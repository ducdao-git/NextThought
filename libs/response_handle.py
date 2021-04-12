import json

from custom_exception import RequestError


def get_response_data(response):
    """
    get the data of a request or raise exception if request is bad
    :param response: a request obj
    :return: response data of the request or None if exception raise
    """
    if response.status_code == 200:
        content = json.loads(response.content)
        # print(response.status_code, '--', content, '--', type(content))
        return content

    elif response.status_code == 400:  # API rejects action
        message = json.loads(response.content)['message']
        raise RequestError(message)

    else:
        raise RequestError("something went wrong")

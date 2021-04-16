from requests.exceptions import RequestException


# Custom Exception used to catch errors when change user data.
class DataError(Exception):
    def __init__(self, error_messages):
        if type(error_messages) in [str, int]:
            self.message = str(error_messages)

        elif type(error_messages) is dict:
            status_code = error_messages.get('status code')

            if status_code == 429:
                self.message = 'Too many requests. Please try again later.'
            else:
                self.message = str(status_code)

        elif isinstance(error_messages, RequestException):
            self.message = 'Unable to connect with the server. Please check ' \
                           'your internet connection or try again later.'

        elif isinstance(error_messages, DataError):
            self.message = error_messages.message

        else:
            self.message = str(type(error_messages))

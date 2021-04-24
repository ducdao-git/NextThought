from requests.exceptions import RequestException


# Custom Exception used to catch errors when change user data.
class DataError(Exception):
    """
    class repr custom exception
    """

    def __init__(self, error_messages):
        """
        create new DataError obj
        :param error_messages: can be any type. depend on the type, the new
        error message will be generate accordingly (read implementation)
        """
        if type(error_messages) in [str, int]:
            self.custom_code = 1
            self.message = str(error_messages)

        elif type(error_messages) is dict:
            status_code = error_messages.get('status code')

            if status_code == 429:
                self.custom_code = 429
                self.message = 'Too many requests. Please try again later.'
            else:
                self.custom_code = status_code
                self.message = str(status_code)

        elif isinstance(error_messages, RequestException):
            self.custom_code = 1
            self.message = 'Unable to connect with the server. Please check ' \
                           'your internet connection or try again later.'

        elif isinstance(error_messages, DataError):
            self.custom_code = error_messages.custom_code
            self.message = error_messages.message

        else:
            self.custom_code = 1
            self.message = str(type(error_messages))

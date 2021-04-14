import requests

from libs.custom_exception import RequestError
from libs.response_handle import get_response_data

api_url = 'http://nsommer.wooster.edu/social'


def create_user(username):
    """
    create a new user in api and AuthorizedUser obj with this username
    :param username: string represent username of new user
    :return: AuthorizedUser obj with this username
    """
    try:
        response = requests.post(api_url + '/users',
                                 data={'username': username})
        response_data = get_response_data(response)

        return AuthorizedUser(username, response_data['token'])

    except RequestError as error:
        print(f'popup create: {error}')


class AuthorizedUser:
    """class represent signed in user"""

    def __init__(self, username, token):
        """
        create new signed in user with username and token, called validation
        upon assign
        :param username: string represent username for the user
        :param token: string represent token / password for the user
        """
        self.uid, self.username = None, None
        self.set_username_id(username)

        self.token = self.set_token(token)

    def set_username_id(self, username):
        """
        setter - set user id and username for the user, check if the username
        exist in the api
        :param username: string represent username for the user
        :return: None
        """
        try:
            response = requests.get(api_url + '/users',
                                    data={'username': username})
            response_data = get_response_data(response)

            if response_data is not None:
                self.uid = response_data['uid']
                self.username = response_data['username']

        except RequestError as error:
            print(f'popup set_id: {username} -- {error}')

    def set_token(self, token):
        """
        setter - check if token is correct then set user token
        :param token: string to check if represent valid token
        :return: string represent token
        """
        # api doesn't ofer check validity of token so test token
        # by change username for an user then change back
        try:
            response = requests.patch(
                api_url + '/users',
                data={'uid': self.uid,
                      'token': token,
                      'username': 'checkToken'}
            )
            get_response_data(response)

            requests.patch(
                api_url + '/users',
                data={'uid': self.uid,
                      'token': token,
                      'username': self.username}
            )
            return token

        except RequestError as error:
            print(f'popup set_token: {self.username} -- {error}')

    def get_username(self):
        """
        getter - get username of current signed in user
        :return: string represent username of current user
        """
        return self.username

    def get_uid(self):
        """
        getter - get uid of current signed in user
        :return: int represent uid of current user
        """
        return self.uid

    def get_token(self):
        """
        getter - get token of current signed in user
        :return: string represent token of current user
        """
        return self.token

    def change_username(self, new_username):
        """
        change username for current signed in user
        :param new_username: string represent new username for the user
        :return: None
        """
        try:
            response = requests.patch(
                api_url + '/users',
                data={'uid': self.uid,
                      'token': self.token,
                      'username': new_username}
            )
            get_response_data(response)

            self.username = new_username

        except RequestError as error:
            print(f'popup change: {self.username} -- {error}')

    def __repr__(self):
        return f'AuthorizedUser class -- uid: {self.uid}, username:' \
               f' {self.username}, token: {self.token}'

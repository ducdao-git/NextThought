import requests

from libs.backend.messages import Message
from libs.backend.custom_exception import DataError
from libs.backend.response_handle import get_response_data

api_url = 'http://nsommer.wooster.edu/social'


def create_user(username):
    """
    create a new user on server and AuthorizedUser obj with this username
    :param username: string represent username of new user
    :return: AuthorizedUser obj with this username
    """
    try:
        response = requests.post(api_url + '/users',
                                 data={'username': username})
        response_data = get_response_data(response)

        return AuthorizedUser(username, response_data['token'])

    except Exception as error:
        print(f'error AUser create user: {error}')
        raise DataError(error)


def get_uid_from_username(username):
    """
    get user ID from the username
    :param username: string repr name of a user
    :return: int repr user ID of the user with this username
    """
    if username in ['', None]:
        return None

    try:
        response = requests.get(api_url + '/users',
                                data={'username': username})
        response_data = get_response_data(response)

        return response_data['uid']

    except Exception as error:
        print(f'error AUser get userID: {error}')
        raise DataError(error)


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
        setter - set user ID and username for the user, check if the username
        exist in the api
        :param username: string represent username for the user
        :return: None
        """
        try:
            response = requests.get(api_url + '/users',
                                    data={'username': username})
            response_data = get_response_data(response)

            self.uid = response_data['uid']
            self.username = response_data['username']

        except Exception as error:
            print(f'error AUser set userID: {error}')
            raise DataError(error)

    def set_token(self, token):
        """
        setter - check if token is correct then set user token
        :param token: string to check if represent valid token
        :return: string represent token
        """
        # api doesn't offer check validity of token so test token
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

        except Exception as error:
            print(f'error AUser set token: {error}')
            raise DataError(error)

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

        except Exception as error:
            print(f'error AUser change name: {error}')
            raise DataError(error)

    def create_message(self, recipientid, message_content):
        """
        try create new message with the sender is this user, recipient is user
        with recipientid. if unable, raise DataError with this error
        :param recipientid: int repr ID of recipient
        :param message_content: string repr content of the new message
        """
        try:
            response = requests.post(
                api_url + '/messages',
                data={
                    'senderid': self.get_uid(),
                    'recipientid': recipientid,
                    'token': self.get_token(),
                    'content': message_content,
                }
            )
            get_response_data(response)

        except Exception as error:
            print(f'error AUser create message: {error}')
            raise DataError(error)

    def get_messages(self, otherid, limit=50):
        """
        try get messages between this user and the other user with otherid. if
        unable, raise DataError with this error
        :param otherid: int repr ID of the other user
        :param limit: int repr number of most recent messages to get
        :return: list of Message obj where each Message obj is a message
        between the 2 users
        """
        try:
            response = requests.get(
                api_url + '/messages',
                data={
                    'uid': self.get_uid(),
                    'otherid': otherid,
                    'token': self.get_token(),
                    'limit': limit
                }
            )
            response_data = get_response_data(response)

            messages = []
            for message in response_data:
                messages.append(Message(
                    sender=message['sender'],
                    senderid=message['senderid'],
                    recipient=message['recipient'],
                    recipientid=message['recipientid'],
                    content=message['content'],
                    time=message['time'],
                ))
            return messages

        except Exception as error:
            print(f'error AUser get messages: {error}')
            raise DataError(error)

    def get_conversations(self):
        """
        try get list of other user that this user has conversation with
        :return: list of ChatPartner obj where each ChatPartner obj represent
        a user that this user has conversation with
        """
        try:
            response = requests.get(
                api_url + '/conversations',
                data={
                    'uid': self.get_uid(),
                    'token': self.get_token()
                }
            )
            response_data = get_response_data(response)

            anonymous_users = []
            for user in response_data:
                anonymous_users.append(
                    ChatPartner(user['username'], user['uid']))

            return anonymous_users

        except Exception as error:
            print(f'error AUser get conversations: {error}')
            raise DataError(error)

    def __repr__(self):
        """
        printable form of AuthorizedUser obj
        :return: string repr AuthorizedUser obj
        """
        return f'AuthorizedUser class -- uid: {self.uid}, username:' \
               f' {self.username}, token: {self.token}'


class ChatPartner:
    """
    class represent anonymous_users. this class only care about username and
    uid of a the user. use when need pass the user who has conversation with
    authorized user around
    """

    def __init__(self, username, uid=None, server_check=False):
        """
        create a new ChatPartner obj. include check validity of username when
        uid is None or server_check is True
        :param username: string repr username for this user
        :param uid: int repr ID of this user
        :param server_check: boolean to do a check validity username and uid
        """
        if server_check or uid is None:
            self.uid = get_uid_from_username(username)

            if self.uid is not None:
                self.username = username
            else:
                self.username = None

        else:
            self.username = username
            self.uid = uid

    def get_username(self):
        """
        getter -- get username
        :return: string repr username of the user
        """
        return self.username

    def get_uid(self):
        """
        getter -- get uid
        :return: int repr ID of the user
        """
        return self.uid

    def __repr__(self):
        """
        printable form of ChatPartner obj
        :return: string repr ChatPartner obj
        """
        return f'ChatPartner class -- uid: {self.uid}, ' \
               f'username: {self.username}'

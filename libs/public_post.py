import requests
from pprint import pprint

from custom_exception import RequestError
from response_handle import get_response_data
from authorized_user import AuthorizedUser

api_url = 'http://nsommer.wooster.edu/social'


def create_public_post(user, content, parentid=-1):
    uid, token = user.get_uid(), user.get_token()

    try:
        response = requests.post(
            api_url + '/posts',
            data={'uid': uid,
                  'token': token,
                  'parentid': parentid,
                  'content': content}
        )
        response_data = get_response_data(response)

        return PublicPost(user, content, response_data['postid'])

    except RequestError as error:
        print(f'popup create_ppost: {error}')


def get_public_posts():
    response = requests.get(api_url + '/posts', data={'tag': 'test'})
    response_data = get_response_data(response)

    pprint(response_data)


class PublicPost:
    def __init__(self, user, content, postid):
        self.uid, self.token = user.get_uid(), user.get_token()
        self.content = content
        self.postid = postid

    def edit_public_post(self, new_content):
        try:
            response = requests.patch(
                api_url + '/posts',
                data={'uid': self.uid,
                      'token': self.token,
                      'postid': self.postid,
                      'content': new_content}
            )
            get_response_data(response)

            self.content = new_content

        except RequestError as error:
            print(f'popup edit_ppost: {self.postid} -- {error}')

    def delete_public_post(self):
        try:
            response = requests.delete(
                api_url + '/posts',
                data={'uid': self.uid,
                      'token': self.token,
                      'postid': self.postid}
            )
            get_response_data(response)

            self.uid = self.token = self.content = self.postid = None

        except RequestError as error:
            print(f'popup del_ppost: {self.postid} -- {error}')

    def __repr__(self):
        return f'AuthorizedUser class -- uid: {self.uid}, ' \
               f'token: {self.token}, content: {self.content}, ' \
               f'postid: {self.postid}'

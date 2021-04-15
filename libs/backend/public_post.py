import requests
from itertools import groupby
from pprint import pprint

from libs.backend.custom_exception import RequestError
from libs.backend.response_handle import get_response_data

api_url = 'http://nsommer.wooster.edu/social'


def create_public_post(user, content, parentid=-1):
    """
    create a new public post in server
    :param user: AuthorizedUser obj who own this post
    :param content: string repr content of the post
    :param parentid: int repr ID of parent post if a comment, else -1
    """
    try:
        response = requests.post(
            api_url + '/posts',
            data={'uid': user.get_uid(),
                  'token': user.get_token(),
                  'parentid': parentid,
                  'content': content}
        )
        get_response_data(response)

    except RequestError as error:
        print(f'popup create_ppost: {error}')
        raise RequestError(error)


def get_public_posts(limit=50, uid=None, tag=None, parent_id=-1):
    """
    get public posts from server then create PublicPost obj from those data
    :param limit: int repr max number of post to fetch
    :param uid: int -- only fetch post from this user ID
    :param tag: string -- only fetch post with this tag
    :param parent_id: int -- only fetch post with this parent, by default fetch
    post that is not comment of other post i.e. parent_id = -1
    :return: list of PublicPost obj from these data
    """
    try:
        response = requests.get(api_url + '/posts',
                                data={'limit': limit, 'uid': uid, 'tag': tag})
        response_data = get_response_data(response)

        sorted_response_data = \
            sorted(response_data, key=lambda x: x['parentid'])

        response_data = {}
        for key, value in groupby(sorted_response_data,
                                  key=lambda x: x['parentid']):
            response_data[key] = list(value)

        public_posts = []
        for post in response_data.get(parent_id, []):
            public_posts.append(
                PublicPost(post['username'], post['content'], post['time'],
                           post['upvotes'],
                           len(response_data.get(post['postid'], [])),
                           post['postid'], post['parentid'])
            )

        return public_posts

    except RequestError as error:
        print(f'popup create_ppost: {error}')
        raise RequestError(error)


class PublicPost:
    def __init__(self, owner_name, content, time, upvotes_num, comments_num,
                 postid, parentid):
        """
        create PublicPost obj with owner name, content and post id
        :param owner_name: string repr name of the owner of this post
        :param content: string repr content of this post
        :param time: string repr posted time for this post
        :param upvotes_num: int repr number of upvote/like for this post
        :param postid: int repr ID of this post
        :param parentid: int repr ID of this post
        """
        self.owner_name = owner_name
        self.content, self.time = content, time
        self.upvotes_num, self.comments_num = upvotes_num, comments_num
        self.postid, self.parentid = postid, parentid

    def get_owner_name(self):
        return self.owner_name

    def get_content(self):
        return self.content

    def get_time(self):
        return self.time

    def get_upvotes_num(self):
        return self.upvotes_num

    def get_comments_num(self):
        return self.comments_num

    def get_postid(self):
        return self.postid

    def get_parentid(self):
        return self.parentid

    def upvote_post(self, user):
        try:
            response = requests.post(
                api_url + '/upvotes',
                data={'uid': user.get_uid(),
                      'token': user.get_token(),
                      'postid': self.postid}
            )
            get_response_data(response)

        except RequestError as error:
            print(f'popup upvote_ppost: {error}')
            raise RequestError(error)

    def edit_public_post(self, owner, new_content):
        """
        edit public post in both server and locally
        :param owner: AuthorizedUser obj repr owner of this post
        :param new_content: string repr the new content of the post
        """
        try:
            response = requests.patch(
                api_url + '/posts',
                data={'uid': owner.get_uid(),
                      'token': owner.get_token(),
                      'postid': self.postid,
                      'content': new_content}
            )
            get_response_data(response)

            self.content = new_content

        except RequestError as error:
            print(f'popup edit_ppost: {self.postid} -- {error}')
            raise RequestError(error)

    def delete_public_post(self, owner):
        """
        delete public post in both server and locally
        :param owner: AuthorizedUser obj repr owner of this post
        """
        try:
            response = requests.delete(
                api_url + '/posts',
                data={'uid': owner.get_uid(),
                      'token': owner.get_token(),
                      'postid': self.postid}
            )
            get_response_data(response)

            self.owner_name = self.content = self.postid = None

        except RequestError as error:
            print(f'popup del_ppost: {self.postid} -- {error}')
            raise RequestError(error)

    def __repr__(self):
        """
        :return: string representation of a public post
        """
        return f'AuthorizedUser class -- owner_name: {self.owner_name}, ' \
               f'content: {self.content}, time: {self.time} ' \
               f'postid: {self.postid}, parentid: {self.parentid}'
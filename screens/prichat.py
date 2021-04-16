from kivy.uix.screenmanager import Screen

from libs.backend.user import get_uid_from_username
from libs.backend.public_post import get_public_posts, create_public_post
from libs.frontend.post_widget import PostView
from libs.backend.custom_exception import DataError
from libs.frontend.custom_popup import FilterPopup, ErrorPopup, \
    PostContentPopup


class PriChatRoute(Screen):
    """
    Screen use to display conversations
    """

    def __init__(self, app, **kwargs):
        """
        :param app: current app instance
        """
        super().__init__(**kwargs)
        self.app = app

    # def on_pre_enter(self, *args):
    #     """
    #     function will be call when the animation to enter the screen start. it
    #     display most <limit> recent post
    #     """
    #     try:
    #         self.display_public_posts(self.filter_username, self.filter_tag)
    #     except DataError as error:
    #         ErrorPopup(error.message).open()
    #
    # def on_leave(self, *args):
    #     """
    #     function will be call whn leaving the screen. the function will clear
    #     all widget in screen i.e. remove all unused widget, data
    #     """
    #     self.ids.newsfeed_scrollview.clear_widgets()
    #
    # def display_public_posts(self, username=None, tag=None):
    #     posts = get_public_posts(uid=get_uid_from_username(username), tag=tag)
    #
    #     for post in posts:
    #         self.ids.newsfeed_scrollview.add_widget(PostView(self, post))
    #
    # def refresh_newsfeed(self):
    #     try:
    #         self.ids.newsfeed_scrollview.clear_widgets()
    #         self.display_public_posts(self.filter_username, self.filter_tag)
    #
    #     except DataError as error:
    #         ErrorPopup(error.message).open()
    #
    # def open_create_post_popup(self):
    #     PostContentPopup(root=self).open()
    #
    # def create_post(self, new_post_content):
    #     if new_post_content in ['', None]:
    #         return None
    #
    #     try:
    #         create_public_post(self.app.authorized_user, new_post_content)
    #         self.refresh_newsfeed()
    #
    #     except DataError as error:
    #         ErrorPopup(error.message).open()
    #
    # def open_filter_popup(self):
    #     FilterPopup(self).open()
    #
    # def filter_post(self, username=None, tag=None):
    #     try:
    #         self.ids.newsfeed_scrollview.clear_widgets()
    #         self.display_public_posts(username, tag)
    #         self.filter_username = username
    #         self.filter_tag = tag
    #
    #     except DataError as error:
    #         ErrorPopup(error.message).open()

from kivy.uix.screenmanager import Screen

from libs.backend.user import get_uid_from_username
from libs.backend.public_post import get_public_posts, create_public_post
from libs.frontend.chat_widget import ChatView
from libs.backend.custom_exception import DataError
from libs.frontend.custom_popup import ErrorPopup


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

    def on_pre_enter(self, *args):
        try:
            self.display_conversations()
        except DataError as error:
            ErrorPopup(error.message).open()

    def on_leave(self, *args):
        self.ids.prichat_scrollview.clear_widgets()

    def display_conversations(self):
        conversations = self.app.authorized_user.get_conversations()

        for other_user in conversations:
            print(other_user)
            self.ids.prichat_scrollview.add_widget(ChatView(self, other_user))

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

from kivy.uix.screenmanager import Screen

from libs.backend.user import get_uid_from_username
from libs.backend.public_post import get_public_posts, create_public_post
from libs.backend.custom_exception import DataError
from libs.frontend.post_widget import PostView
from libs.frontend.custom_popup import *


class NewsfeedRoute(Screen):
    """
    Screen use to display public posts
    """

    def __init__(self, app, **kwargs):
        """
        :param app: current app instance
        """
        super().__init__(**kwargs)
        self.app = app
        self.filter_username = None
        self.filter_tag = None
        self.num_post_show = self.app.user_profile.get_num_post_show()

    def on_pre_enter(self, *args):
        """
        function will be call when the animation to enter the screen start. it
        display most <limit> recent post
        """
        try:
            self.display_public_posts(self.filter_username, self.filter_tag)
        except DataError as error:
            ErrorPopup(error.message).open()

    def on_leave(self, *args):
        """
        function will be call whn leaving the screen. the function will clear
        all widget in screen i.e. remove all unused widget, data
        """
        self.ids.newsfeed_scrollview.clear_widgets()

    def display_public_posts(self, username=None, tag=None):
        posts = get_public_posts(
            limit=self.num_post_show,
            uid=get_uid_from_username(username),
            tag=tag
        )

        # print(posts)

        for post in posts:
            self.ids.newsfeed_scrollview.add_widget(PostView(self, post))

    def refresh_display(self):
        try:
            self.ids.newsfeed_scrollview.clear_widgets()
            self.display_public_posts(self.filter_username, self.filter_tag)

        except DataError as error:
            ErrorPopup(error.message).open()

    def open_create_post_popup(self):
        OneInputFieldPopup(screen_instance=self).open()

    def create_post(self, new_post_content):
        if new_post_content in ['', None]:
            return None

        try:
            create_public_post(self.app.authorized_user, new_post_content)
            self.refresh_display()

        except DataError as error:
            ErrorPopup(error.message).open()

    def open_filter_popup(self):
        FilterPopup(self).open()

    def filter_post(self, username=None, tag=None):
        try:
            self.ids.newsfeed_scrollview.clear_widgets()
            self.display_public_posts(username, tag)
            self.filter_username = username
            self.filter_tag = tag

        except DataError as error:
            if error.message == 'No such user':
                self.refresh_display()

            ErrorPopup(error.message).open()

    def open_setting_popup(self):
        SettingPopup(self).open()

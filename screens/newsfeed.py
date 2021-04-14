from kivy.uix.screenmanager import Screen

from libs.authorized_user import get_uid_from_username
from libs.public_post import get_public_posts
from libs.post_widget import PostView
from libs.custom_popup import SearchPopup


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

    def on_pre_enter(self, *args):
        """
        function will be call when the animation to enter the screen start. it
        display most <limit> recent post
        """
        self.display_public_posts()

    def on_leave(self, *args):
        """
        function will be call whn leaving the screen. the function will clear
        all widget in screen i.e. remove all unused widget, data
        """
        self.ids.newsfeed_scrollview.clear_widgets()

    def display_public_posts(self, username=None, tag=None):
        posts = get_public_posts(uid=get_uid_from_username(username), tag=tag)
        # pprint(posts)

        for post in posts:
            self.ids.newsfeed_scrollview.add_widget(PostView(self, post))

    def delete_post(self, postview_instance):
        self.ids.newsfeed_scrollview.remove_widget(postview_instance)

    def edit_post(self):
        self.ids.newsfeed_scrollview.clear_widgets()
        self.display_public_posts(self.filter_username, self.filter_tag)

    def open_filter_popup(self):
        SearchPopup(self).open()

    def filter_post(self, username=None, tag=None):
        self.filter_username = username
        self.filter_tag = tag
        self.ids.newsfeed_scrollview.clear_widgets()
        self.display_public_posts(username, tag)

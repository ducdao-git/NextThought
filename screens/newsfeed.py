from pprint import pprint

from kivy.uix.screenmanager import Screen

from libs.public_post import get_public_posts
from libs.post_widget import PostView


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

    def display_public_posts(self):
        posts = get_public_posts()
        # pprint(posts)

        for post in posts:
            self.ids.newsfeed_scrollview.add_widget(PostView(self, post))

    def delete_post(self, postview_instance):
        self.ids.newsfeed_scrollview.remove_widget(postview_instance)

    def edit_post(self):
        print('edit_post')
        self.ids.newsfeed_scrollview.clear_widgets()
        self.display_public_posts()

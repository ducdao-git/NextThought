from kivy.uix.screenmanager import Screen

from libs.backend.user import get_uid_from_username
from libs.backend.public_post import get_public_posts, create_public_post
from libs.frontend.post_widget import PostView
from libs.frontend.custom_popup import *


class NewsfeedRoute(Screen):
    """
    screen use to display public posts
    """

    def __init__(self, app, **kwargs):
        """
        :param app: current app instance
        :param kwargs: param call for Screen class
        """
        super().__init__(**kwargs)
        self.app = app
        self.user_profile = self.app.user_profile
        self.filter_username = None
        self.filter_tag = None

    def on_pre_enter(self, *_):
        """
        call display_public_posts() when enter to this screen. if
        display_public_posts raise DataError, then display the error
        """
        try:
            self.display_public_posts(self.filter_username, self.filter_tag)
        except DataError as error:
            ErrorPopup(error.message).open()

    def on_leave(self, *_):
        """
        empty the screen scrollview when enter to different screen
        """
        self.ids.newsfeed_scrollview.clear_widgets()

    def display_public_posts(self, username=None, tag=None):
        """
        display most <limit> recent posts
        :param username: string repr name of user to filter and take only posts
        that post by this user. if None, take all available posts
        :param tag: string repr tag and take only posts contain this tag. if
        None, take all available posts
        """
        posts = get_public_posts(
            limit=self.user_profile.get_num_post_show(),
            uid=get_uid_from_username(username),
            tag=tag
        )

        if len(posts) == 0:
            self.ids.show_no_post.visible = True
        else:
            self.ids.show_no_post.visible = False

        for post in posts:
            self.ids.newsfeed_scrollview.add_widget(PostView(self, post))

    def refresh_display(self):
        """
        clear the posts data then re-display to display the newest post
        (refresh functionality). display error if unable to display newest
        public posts
        """
        try:
            self.ids.newsfeed_scrollview.clear_widgets()
            self.display_public_posts(self.filter_username, self.filter_tag)

        except DataError as error:
            ErrorPopup(error.message).open()

    def open_create_post_popup(self):
        """
        open popup to take in content for new post
        """
        OneInputFieldPopup(screen_instance=self).open()

    def create_post(self, new_post_content):
        """
        create a new post on server then refresh the display to get update
        :param new_post_content: string repr content of new post and create new
        post on server with this content. display error if unable to create new
        post
        """
        if new_post_content in ['', None]:
            return None

        try:
            create_public_post(self.app.authorized_user, new_post_content)
            self.refresh_display()

        except DataError as error:
            ErrorPopup(error.message).open()

    def open_filter_popup(self):
        """
        open filter popup for to enter filter option
        """
        FilterPopup(self).open()

    def filter_post(self, username=None, tag=None):
        """
        take in username and tag for filter, try to display posts that pass
        these filter. if able to display post then set screen wide filter
        username and tag. if unable, then display error
        :param username: string repr name of user to pass to
        display_public_posts()
        :param tag: string repr tag to pass to display_public_posts()
        """
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
        """open setting popup"""
        SettingPopup(self).open()

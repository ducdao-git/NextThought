from kivy.uix.screenmanager import Screen

from libs.backend.custom_exception import DataError
from libs.backend.public_post import create_public_post, get_public_posts
from libs.frontend.comment_widget import TopCommentView, CommentView
from libs.frontend.custom_popup import ErrorPopup


class CommentsRoute(Screen):
    # might notice that this screen along with it support widget is really
    # similar to newsfeed screen but they have really different look and some
    # different functionality here and there thus I split it to a new class
    """
    screen use to display comments
    """

    def __init__(self, app, **kwargs):
        """
        :param app: current app instance
        :param kwargs: param call for Screen class
        """
        super().__init__(**kwargs)
        self.app = app
        self.user_profile = self.app.user_profile
        self.top_comment = None
        self.comments = None

    def on_pre_enter(self, *_):
        """
        call display_comments() when enter this screen
        """
        # ScreenManager remove_widget will go in screen before delete thus
        # trigger on_pre_enter when requirement not meet
        if self.app.process_post is None:
            return

        self.display_comments()

    def on_leave(self, *_):
        """
        clear the scrollview when leave the screen
        """
        self.ids.comment_scrollview.clear_widgets()

    def refresh_display(self):
        """
        re-display the newest comments from the server
        """
        self.ids.comment_scrollview.clear_widgets()
        self.display_comments()

    def display_comments(self):
        """
        try to display comments. if unable, display error
        """
        try:
            self.top_comment = self.app.process_post

            self.ids.comment_scrollview.add_widget(
                TopCommentView(self, self.top_comment))

            self.comments = get_public_posts(
                limit=self.user_profile.get_num_post_show(),
                parent_id=self.top_comment.get_postid())

            for comment in self.comments:
                self.ids.comment_scrollview.add_widget(
                    CommentView(self, comment))

        except DataError as error:
            ErrorPopup(error.message).open()

    def create_comment(self):
        """
        create a new comment with user input date on the server. auto take new
        comment content from comment_content_input then remove left and right
        empty space
        """
        try:
            comment_input = self.ids.comment_content_input.text.strip()

            if comment_input in ['', None]:
                return

            create_public_post(
                user=self.app.authorized_user,
                content=comment_input,
                parentid=self.top_comment.get_postid()
            )

            self.top_comment.reduce_comments_num(-1)
            self.refresh_display()
            self.ids.comment_content_input.text = ''

        except DataError as error:
            ErrorPopup(error.message).open()

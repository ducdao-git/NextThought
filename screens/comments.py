from kivy.uix.screenmanager import Screen

from libs.backend.custom_exception import DataError
from libs.backend.public_post import create_public_post, get_public_posts
from libs.frontend.comment_widget import TopCommentView, CommentView
from libs.frontend.custom_popup import ErrorPopup


class CommentsRoute(Screen):
    def __init__(self, app, **kwargs):
        """
        :param app: current app instance
        """
        super().__init__(**kwargs)
        self.app = app
        self.top_comment = None
        self.comments = None

    def on_pre_enter(self, *args):
        self.display_comments()

    def on_leave(self, *args):
        self.ids.comment_scrollview.clear_widgets()

    def refresh_display(self):
        self.ids.comment_scrollview.clear_widgets()
        self.display_comments()

    def display_comments(self):
        try:
            self.top_comment = self.app.process_post

            self.ids.comment_scrollview.add_widget(
                TopCommentView(self, self.top_comment))

            self.comments = get_public_posts(
                parent_id=self.top_comment.get_postid())

            for comment in self.comments:
                self.ids.comment_scrollview.add_widget(
                    CommentView(self, comment))

        except DataError as error:
            ErrorPopup(error.message).open()

    def create_comment(self):
        try:
            comment_input = self.ids.comment_content_input.text

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

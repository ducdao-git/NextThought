from kivy.uix.screenmanager import Screen

from libs.backend.public_post import get_public_posts
from libs.frontend.comment_widget import TopCommentView, CommentView


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
        self.top_comment = self.app.process_post

        self.ids.comment_scrollview.add_widget(
            TopCommentView(self, self.top_comment))

        self.comments = get_public_posts(
            parent_id=self.top_comment.get_postid())

        for comment in self.comments:
            self.ids.comment_scrollview.add_widget(CommentView(self, comment))

    def on_leave(self, *args):
        self.ids.comment_scrollview.clear_widgets()

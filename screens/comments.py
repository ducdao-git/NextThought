from kivy.uix.screenmanager import Screen

from libs.backend.public_post import get_public_posts
from libs.frontend.comment_widget import CommentOptionButton
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
        print('on_pre_enter')
        self.top_comment = self.app.process_post

        self.ids.comment_scrollview.add_widget(
            TopCommentView(self, self.top_comment))

        self.comments = get_public_posts(
            parent_id=self.top_comment.get_postid())

        for comment in self.comments:
            self.ids.comment_scrollview.add_widget(CommentView(self, comment))

    # def on_leave(self, *args):
    #     self.ids.top_comment_option_holder.clear_widgets()

    # def comment_edit(self, comment_new_content):
    #     self.top_comment.edit_public_post(self.app.authorized_user,
    #                                       comment_new_content)
    #
    # def top_comment_delete(self):
    #     self.top_comment.delete_public_post(self.app.authorized_user)
    #     self.app.route_manager.current = \
    #         self.app.route_manager.return_route

from kivy.uix.screenmanager import Screen

from libs.frontend.post_widget import PostOptionButton


class CommentsRoute(Screen):
    def __init__(self, app, **kwargs):
        """
        :param app: current app instance
        """
        super().__init__(**kwargs)
        self.app = app

    def on_pre_enter(self, *args):
        top_post = self.app.process_post

        self.ids.top_comment_owner_name.text = \
            f'[b]{top_post.get_owner_name()}[/b]'

        if self.app.authorized_user.get_username() == \
                top_post.get_owner_name():
            self.ids.row.add_widget(PostOptionButton(self, 'edit'))
            self.ids.row.add_widget(PostOptionButton(self, 'delete'))

        self.ids.top_comment_content.text = top_post.get_content()

    def on_leave(self, *args):
        for i in range(2):
            self.ids.row.clear_widgets()

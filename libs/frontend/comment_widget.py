from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import CardTransition

from libs.backend.local_data_handle import get_readable_time
from libs.backend.custom_exception import DataError
from libs.frontend.custom_kv_widget import IconButton
from libs.frontend.custom_popup import PostContentPopup, ErrorPopup


class CommentOptionButton(IconButton):
    def __init__(self, commentview_instance, option_action, **kwargs):
        super().__init__(**kwargs)
        self.option_action = option_action
        self.commentview_instance = commentview_instance

        if option_action in ['edit_comment', 'edit_top_comment']:
            option_icon = self.edit_icon
        elif option_action in ['delete_comment', 'delete_top_comment']:
            option_icon = self.delete_icon
        else:
            option_icon = self.error_icon

        self.text = f'[size=16sp]{option_icon}[/size]'

    def on_release(self):
        if self.option_action in ['edit_comment', 'edit_top_comment']:
            return PostContentPopup(
                postview_instance=self.commentview_instance,
                action_name=self.option_action
            ).open()

        elif self.option_action == 'delete_top_comment':
            return self.commentview_instance.top_comment_delete()

        elif self.option_action == 'delete_comment':
            return self.commentview_instance.comment_delete()

        else:
            return None


class TopCommentView(BoxLayout):
    def __init__(self, screen_instance, comment, **kwargs):
        super().__init__(**kwargs)
        self.screen_instance = screen_instance
        self.comment = comment
        self.comment_upvote_count = self.comment.get_upvotes_num()
        self.post_new_content = 'comment edit -- sth go wrong'

        self.ids.top_comment_owner_name.text = \
            f'[b]{self.comment.get_owner_name()}[/b]'

        if self.screen_instance.app.authorized_user.get_username() == \
                self.comment.get_owner_name():
            self.ids.top_comment_option_holder.add_widget(
                CommentOptionButton(self, 'edit_top_comment'))
            self.ids.top_comment_option_holder.add_widget(
                CommentOptionButton(self, 'delete_top_comment'))

        self.ids.top_comment_content.text = self.comment.get_content()

        self.ids.top_comment_upvote_num.text = \
            self.ids.top_comment_upvote_num.icon + \
            f' [size=14sp]{self.comment_upvote_count}[/size]'

        self.ids.top_comment_comment_num.text = \
            self.ids.top_comment_comment_num.icon + \
            f' [size=14sp]{self.comment.get_comments_num()}[/size]'

        self.ids.top_comment_time.text = \
            get_readable_time(self.comment.get_time())

    def top_comment_edit(self, comment_new_content):
        if comment_new_content == '':
            return
        try:
            self.comment.edit_public_post(
                self.screen_instance.app.authorized_user, comment_new_content)

            self.ids.top_comment_content.text = comment_new_content

        except DataError as error:
            ErrorPopup(error.message).open()

    def top_comment_delete(self):
        try:
            self.comment.delete_public_post(
                self.screen_instance.app.authorized_user)

            self.screen_instance.app.route_manager.transition = \
                CardTransition(mode='pop', direction='down')
            self.screen_instance.app.route_manager.current = \
                self.screen_instance.app.route_manager.return_route

        except DataError as error:
            ErrorPopup(error.message).open()

    def top_comment_upvote(self):
        try:
            self.comment.upvote_post(self.screen_instance.app.authorized_user)
            self.comment_upvote_count += 1

            self.ids.top_comment_upvote_num.text = \
                self.ids.top_comment_upvote_num.icon + \
                f' [size=14sp]{self.comment_upvote_count}[/size]'

        except DataError as error:
            ErrorPopup(error.message).open()

    def focus_new_comment_input(self):
        self.screen_instance.ids.comment_content_input.focus = True


class CommentView(BoxLayout):
    def __init__(self, screen_instance, comment, **kwargs):
        super().__init__(**kwargs)
        self.screen_instance = screen_instance
        self.comment = comment
        self.upvote_count = self.comment.get_upvotes_num()
        self.post_new_content = 'comment edit -- sth go wrong'

        self.ids.comment_owner_name.text = \
            f'[b]{self.comment.get_owner_name()}[/b]'

        if self.screen_instance.app.authorized_user.get_username() == \
                self.comment.get_owner_name():
            self.ids.comment_option_holder.add_widget(
                CommentOptionButton(self, 'edit_comment'))
            self.ids.comment_option_holder.add_widget(
                CommentOptionButton(self, 'delete_comment'))

        self.ids.comment_content.text = self.comment.get_content()

        self.ids.comment_upvote_num.text = \
            self.ids.comment_upvote_num.icon + \
            f' [size=14sp]{self.upvote_count}[/size]'

        self.ids.comment_comment_num.text = \
            self.ids.comment_comment_num.icon + \
            f' [size=14sp]{self.comment.get_comments_num()}[/size]'

        self.ids.comment_time.text = get_readable_time(self.comment.get_time())

    def comment_delete(self):
        try:
            self.comment.delete_public_post(
                self.screen_instance.app.authorized_user)

            self.screen_instance.top_comment.reduce_comments_num()
            self.screen_instance.refresh_display()

        except DataError as error:
            ErrorPopup(error.message).open()

    def comment_edit(self, comment_new_content):
        if comment_new_content in ['', None]:
            return

        try:
            self.comment.edit_public_post(
                self.screen_instance.app.authorized_user,
                comment_new_content)

            self.ids.comment_content.text = comment_new_content

        except DataError as error:
            ErrorPopup(error.message).open()

    def comment_upvote(self):
        try:
            self.comment.upvote_post(self.screen_instance.app.authorized_user)
            self.upvote_count += 1

            self.ids.comment_upvote_num.text = \
                self.ids.comment_upvote_num.icon + \
                f' [size=14sp]{self.upvote_count}[/size]'

        except DataError as error:
            ErrorPopup(error.message).open()

    def display_comment_reply(self):
        try:
            self.screen_instance.app.process_post = self.comment
            self.screen_instance.refresh_display()

        except DataError as error:
            ErrorPopup(error.message).open()

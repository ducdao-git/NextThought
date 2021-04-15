from kivy.uix.boxlayout import BoxLayout

from libs.frontend.custom_kv_widget import IconButton
from libs.frontend.custom_popup import PostContentPopup


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


class CommentView(BoxLayout):
    def __init__(self, screen_instance, comment, **kwargs):
        super().__init__(**kwargs)
        self.screen_instance = screen_instance
        self.comment = comment
        self.comment_upvote_count = self.comment.get_upvotes_num()
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
            f' [size=14sp]{self.comment_upvote_count}[/size]'

        self.ids.comment_comment_num.text = \
            self.ids.comment_comment_num.icon + \
            f' [size=14sp]{self.comment.get_comments_num()}[/size]'

    def comment_delete(self):
        self.comment.delete_public_post(
            self.screen_instance.app.authorized_user)
        self.screen_instance.ids.comment_scrollview.remove_widget(self)


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

    def top_comment_edit(self, comment_new_content):
        if comment_new_content == '':
            return

        self.comment.edit_public_post(
            self.screen_instance.app.authorized_user, comment_new_content)
        self.ids.top_comment_content.text = comment_new_content

    def top_comment_delete(self):
        self.comment.delete_public_post(
            self.screen_instance.app.authorized_user)
        self.screen_instance.app.route_manager.current = \
            self.screen_instance.app.route_manager.return_route

    def top_comment_upvote(self):
        self.comment.upvote_post(self.screen_instance.app.authorized_user)
        self.comment_upvote_count += 1
        self.ids.top_comment_upvote_num.text = \
            self.ids.top_comment_upvote_num.icon + \
            f' [size=14sp]{self.comment_upvote_count}[/size]'

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import CardTransition

from libs.backend.local_data_handle import get_readable_time
from libs.backend.custom_exception import DataError
from libs.frontend.custom_kv_widget import IconButton
from libs.frontend.custom_popup import OneInputFieldPopup, ErrorPopup


class CommentOptionButton(IconButton):
    """
    class use to display option for comment. only display this class if the
    AuthorizedUser is the owner of the comment
    """

    def __init__(self, commentview_instance, option_action, **kwargs):
        """
        create CommentOptionButton obj. depend on option_action, the button
        will have different icon and functionality
        :param commentview_instance: BoxLayout obj repr view that will hold
        this option button
        :param option_action: string repr name of the action
        :param kwargs: param call for Button class
        """
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
        """
        on release call the according function in the commentview instance or
        open popup for edit_comment and edit_top_comment action
        """
        if self.option_action in ['edit_comment', 'edit_top_comment']:
            return OneInputFieldPopup(view_instance=self.commentview_instance,
                                      action_name=self.option_action).open()

        elif self.option_action == 'delete_top_comment':
            return self.commentview_instance.top_comment_delete()

        elif self.option_action == 'delete_comment':
            return self.commentview_instance.comment_delete()

        else:
            return None


class TopCommentView(BoxLayout):
    """
    class use to display a top comment i.e. comment that the screen will
    display only sub-comment to this comment bellow
    """

    def __init__(self, screen_instance, comment, **kwargs):
        """
        :param screen_instance: Screen obj repr screen that will display this
        TopCommentView obj
        :param comment: PublicPost obj repr a comment
        :param kwargs: param call for BoxLayout class
        """
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
        """
        try edit the top comment. if unable, display error
        :param comment_new_content: string repr new content for the comment
        """
        if comment_new_content == '':
            return
        try:
            self.comment.edit_public_post(
                self.screen_instance.app.authorized_user, comment_new_content)

            self.ids.top_comment_content.text = comment_new_content

        except DataError as error:
            ErrorPopup(error.message).open()

    def top_comment_delete(self):
        """
        try delete the top comment. if unable, display error
        """
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
        """
        try upvote top comment. if unable, display error
        """
        try:
            self.comment.upvote_post(self.screen_instance.app.authorized_user)
            self.comment_upvote_count += 1

            self.ids.top_comment_upvote_num.text = \
                self.ids.top_comment_upvote_num.icon + \
                f' [size=14sp]{self.comment_upvote_count}[/size]'

        except DataError as error:
            ErrorPopup(error.message).open()

    def focus_new_comment_input(self):
        """
        auto focus the input to the input field for the top comment
        """
        self.screen_instance.ids.comment_content_input.focus = True


class CommentView(BoxLayout):
    """
    class use to display a comment
    """

    def __init__(self, screen_instance, comment, **kwargs):
        """
        :param screen_instance: Screen obj repr screen that will display this
        CommentView obj
        :param comment: PublicPost obj repr a comment
        :param kwargs: param call for BoxLayout class
        """
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
        """
        try delete a comment. if unable, display error
        """
        try:
            self.comment.delete_public_post(
                self.screen_instance.app.authorized_user)

            self.screen_instance.top_comment.reduce_comments_num()
            self.screen_instance.refresh_display()

        except DataError as error:
            ErrorPopup(error.message).open()

    def comment_edit(self, comment_new_content):
        """
        try edit a comment. if unable, display error
        :param comment_new_content: string repr new content for the comment
        """
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
        """
        try upvote a comment. if unable, display error
        """
        try:
            self.comment.upvote_post(self.screen_instance.app.authorized_user)
            self.upvote_count += 1

            self.ids.comment_upvote_num.text = \
                self.ids.comment_upvote_num.icon + \
                f' [size=14sp]{self.upvote_count}[/size]'

        except DataError as error:
            ErrorPopup(error.message).open()

    def display_comment_reply(self):
        """
        try display reply to a comment i.e. sub-comment of a comment. if
        unable, display error
        """
        try:
            self.screen_instance.app.process_post = self.comment
            self.screen_instance.refresh_display()

        except DataError as error:
            ErrorPopup(error.message).open()

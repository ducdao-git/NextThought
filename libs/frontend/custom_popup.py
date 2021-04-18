from kivy.uix.modalview import ModalView
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock

from libs.backend.custom_exception import DataError


class FilterPopup(ModalView):
    def __init__(self, screen_instance, **kwargs):
        super().__init__(**kwargs)
        self.screen_instance = screen_instance

        if self.screen_instance.filter_username not in ['', None]:
            self.ids.filter_username.text = \
                self.screen_instance.filter_username

        if self.screen_instance.filter_tag not in ['', None]:
            self.ids.filter_tag.text = self.screen_instance.filter_tag

    def on_dismiss(self):
        filter_username, filter_tag = None, None

        if self.ids.filter_username.text != '':
            filter_username = self.ids.filter_username.text.strip()

        if self.ids.filter_tag.text != '':
            filter_tag = self.ids.filter_tag.text.lstrip('#').strip()

        self.screen_instance.filter_post(filter_username, filter_tag)


class OneInputFieldPopup(ModalView):
    def __init__(self, screen_instance=None, view_instance=None,
                 action_name='create_post', **kwargs):
        super().__init__(**kwargs)
        self.view_instance = view_instance
        self.screen_instance = screen_instance
        self.action_name = action_name

        if action_name == 'edit_post':
            self.ids.popup_title.text = 'Edit post'
            self.ids.input_field.text = \
                self.view_instance.post.get_content()

        elif action_name == 'create_post':
            self.ids.input_field.text = ''

        elif action_name in ['edit_comment', 'edit_top_comment']:
            self.ids.popup_title.text = 'Edit post'
            self.ids.input_field.text = \
                self.view_instance.comment.get_content()

        elif action_name == 'find_partner':
            self.size_hint = (0.7, 1)
            self.ids.popup_title.text = 'Stat conversation with'
            self.ids.input_icon.text = self.user_icon
            self.ids.input_field.hint_text = 'Type a username...'

    def on_dismiss(self):
        if self.action_name == 'edit_post':
            self.view_instance.post_edit(self.ids.input_field.text.strip())

        elif self.action_name == 'create_post':
            self.screen_instance.create_post(self.ids.input_field.text.strip())

        elif self.action_name == 'edit_top_comment':
            self.view_instance.top_comment_edit(
                self.ids.input_field.text.strip())

        elif self.action_name == 'edit_comment':
            self.view_instance.comment_edit(
                self.ids.input_field.text.strip())

        elif self.action_name == 'find_partner':
            self.screen_instance.get_partner(
                self.ids.input_field.text.strip())


class ErrorPopup(ModalView):
    """
    custom error popup
    """

    def __init__(self, message, **kwargs):
        """
        create a popup with this message
        :param message: string as message will be display
        """
        super().__init__(**kwargs)
        self.ids.error_popup_message.text = message


class SuccessSignUpPopup(ModalView):
    def __init__(self, screen_instance, acc_password, **kwargs):
        super().__init__(**kwargs)
        self.acc_password = acc_password
        self.screen_instance = screen_instance

        self.display_password()

    def copy_password(self):
        Clipboard.copy(self.acc_password)

        self.ids.password_display.text = \
            f'[color={self.good_color}]copied![/color]'

        Clock.schedule_once(lambda *_: self.display_password(), 1)

    def display_password(self):
        self.ids.password_display.text = f'[b]{self.acc_password}[/b]'


class SettingPopup(ModalView):
    def __init__(self, screen_instance, **kwargs):
        super().__init__(**kwargs)
        self.screen_instance = screen_instance
        self.user_profile = self.screen_instance.app.user_profile

    def show_help(self, field_name):
        if self.ids[field_name].text == '' and field_name == 'msg_num_help':
            self.ids[field_name].text = \
                'Maximum number of message will show when ' \
                'in a chat (0 < number < 101)'
        elif self.ids[field_name].text == '' and field_name == 'post_num_help':
            self.ids[field_name].text = \
                'Maximum number of posts or comments will show when ' \
                'view the newsfeed or post\'s comments (0 < number < 101)'
        else:
            return

    def update_user_profile(self):
        try:
            if not self.ids.post_num_input.text.strip() == '':
                self.user_profile.set_num_post_show(
                    self.ids.post_num_input.text.strip())

            if not self.ids.msg_num_input.text.strip() == '':
                self.user_profile.set_num_message_show(
                    self.ids.msg_num_input.text.strip())

            self.dismiss()

        except DataError as error:
            ErrorPopup(error.message).open()

    def on_dismiss(self):
        if self.screen_instance.name == 'newsfeed_route':
            self.screen_instance.refresh_display()

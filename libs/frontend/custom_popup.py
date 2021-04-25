from kivy.uix.modalview import ModalView
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock

from libs.backend.custom_exception import DataError
from libs.backend.local_data_handle import get_theme_palette


class FilterPopup(ModalView):
    """
    class use to display filter option as a popup
    """

    def __init__(self, screen_instance, **kwargs):
        """
        :param screen_instance: Screen obj repr screen that will display this
        FilterPopup obj
        :param kwargs: param call for ModalView class
        """
        super().__init__(**kwargs)
        self.screen_instance = screen_instance

        if self.screen_instance.filter_username not in ['', None]:
            self.ids.filter_username.text = \
                self.screen_instance.filter_username

        if self.screen_instance.filter_tag not in ['', None]:
            self.ids.filter_tag.text = self.screen_instance.filter_tag

    def on_dismiss(self):
        """
        give input data and call filter_post function from screen instance when
        dismiss
        """
        filter_username, filter_tag = None, None

        if self.ids.filter_username.text != '':
            filter_username = self.ids.filter_username.text.strip()

        if self.ids.filter_tag.text != '':
            filter_tag = self.ids.filter_tag.text.lstrip('#').strip()

        self.screen_instance.filter_post(filter_username, filter_tag)


class OneInputFieldPopup(ModalView):
    """
    class use to display popup with exactly one input field
    """

    def __init__(self, screen_instance=None, view_instance=None,
                 action_name='create_post', **kwargs):
        """
        create OneInputFieldPopup obj. action_name will also affect what the
        popup will display
        :param screen_instance: Screen obj repr screen that will display this
        OneInputFieldPopup obj
        :param view_instance: BoxLayout obj which will display this
        OneInputFieldPopup obj
        :param action_name: string repr name of the action
        :param kwargs: param call for ModalView class
        """
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
        """
        call appropriate function when popup get dismiss. depend on the
        action_name, the screen_instance or view_instance will need to run the
        action functionality.
        """
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
    """
    class use to display successful sign up message when sign up is success
    """

    def __init__(self, screen_instance, acc_password, **kwargs):
        """
        :param screen_instance: Screen obj repr screen that will display this
        SuccessSignUpPopup obj
        :param acc_password: string repr token of the sign up account
        :param kwargs: param call for ModalView class
        """
        super().__init__(**kwargs)
        self.acc_password = acc_password
        self.screen_instance = screen_instance

        self.display_password()

    def copy_password(self):
        """
        allow user to click on the password to copy. change the text to
        'copied!' to notice user the password has copied
        """
        Clipboard.copy(self.acc_password)

        self.ids.password_display.text = \
            f'[color={self.good_color}]copied![/color]'

        Clock.schedule_once(lambda *_: self.display_password(), 1)

    def display_password(self):
        """
        display token for the new sign up account
        """
        self.ids.password_display.text = f'[b]{self.acc_password}[/b]'


class SettingPopup(ModalView):
    """
    class use to display the setting
    """

    def __init__(self, screen_instance, **kwargs):
        """
        :param screen_instance: Screen obj repr screen that will display this
        SettingPopup obj
        :param kwargs: param call for ModalView class
        """
        super().__init__(**kwargs)
        self.screen_instance = screen_instance
        self.app = self.screen_instance.app
        self.user_profile = self.screen_instance.app.user_profile

        if self.user_profile.get_theme_name() == 'light':
            self.ids.light_theme.bg_color = \
                self.ids.theme_option.selected_bg_color
            self.ids.light_theme.color = \
                self.ids.theme_option.selected_text_color

        elif self.user_profile.get_theme_name() == 'dark':
            self.ids.dark_theme.bg_color = \
                self.ids.theme_option.selected_bg_color
            self.ids.dark_theme.color = \
                self.ids.theme_option.selected_text_color

    def show_help(self, field_name):
        """
        show help for input field. help the user understand what this value do
        :param field_name: string repr the name of the input field we need to
        show help for
        """
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
        """
        update user profile with the new user input data. if unable to set
        value to any option, display error
        """
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

    def change_theme(self, new_theme_name):
        self.user_profile.set_theme_name(new_theme_name)
        self.app.theme_palette = get_theme_palette(new_theme_name)
        self.app.refresh_theme()

    def on_dismiss(self):
        """
        on dismiss, depend on the screen, will refresh if the screen is
        newsfeed or message
        """
        if self.screen_instance.name == 'newsfeed_route':
            self.screen_instance.refresh_display()
        if self.screen_instance.name == 'message_route':
            self.screen_instance.refresh_messages()

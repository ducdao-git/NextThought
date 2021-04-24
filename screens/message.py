from time import sleep

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from libs.backend.local_data_handle import get_readable_time
from libs.backend.custom_exception import DataError
from libs.frontend.chat_widget import UserMessageView, PartnerMessageView
from libs.frontend.custom_popup import ErrorPopup, SettingPopup


class MessageRoute(Screen):
    """
    screen display conversation between 2 user
    """

    def __init__(self, app, **kwargs):
        """
        :param app: current app instance
        :param kwargs: param call for Screen class
        """
        super().__init__(**kwargs)
        self.app = app
        self.user_profile = self.app.user_profile
        self.authorized_user = None
        self.message_partner = None

    def on_pre_enter(self, *_):
        """
        update 2 user object repr the 2 user in this conversation and display
        the message between them when enter this screen
        """
        self.authorized_user = self.app.authorized_user
        self.message_partner = self.app.process_message_partner

        self.ids.message_partner_name.text = \
            self.message_partner.get_username()

        self.display_messages()

    def on_leave(self, *_):
        """
        clear message between the 2 users and the input fields when leave the
        screen
        """
        self.ids.message_scrollview.clear_widgets()
        self.ids.message_content_input.text = ''

    def refresh_messages(self):
        """
        re-display the newest message between the 2 users
        """
        self.ids.message_scrollview.clear_widgets()
        self.display_messages()

    def display_messages(self):
        """
        try to display messages between 2 users. if request code is 429, auto
        retry. if unable to display, display error.
        """
        try:
            messages = self.authorized_user.get_messages(
                self.message_partner.get_uid(),
                limit=self.user_profile.get_num_message_show(),
            )

            if len(messages) == 0:
                return

            for message in messages[::-1]:
                if message.get_senderid() == self.authorized_user.get_uid():
                    self.ids.message_scrollview.add_widget(
                        UserMessageView(
                            message.get_content(),
                            get_readable_time(message.get_time(), True)
                        ))
                else:
                    self.ids.message_scrollview.add_widget(
                        PartnerMessageView(
                            message.get_content(),
                            get_readable_time(message.get_time(), True)
                        ))

            empty_label = Label(size_hint=(1, None), height=0)
            self.ids.message_scrollview.add_widget(empty_label)
            self.ids.scrollview_widget.scroll_to(empty_label)

        except DataError as error:
            if error.custom_code == 429:
                sleep(0.05)
                self.display_messages()
            else:
                ErrorPopup(error.message).open()

    def create_message(self):
        """
        create new message on server. auto take content from the
        message_content_input field and clear it if able to create the message.
        if unable, display error
        """
        if self.ids.message_content_input.text in ['', None]:
            return

        try:
            self.authorized_user.create_message(
                self.message_partner.get_uid(),
                self.ids.message_content_input.text.strip()
            )

            self.ids.message_scrollview.clear_widgets()
            self.display_messages()
            self.ids.message_content_input.text = ''

        except DataError as error:
            ErrorPopup(error.message).open()

    def open_setting_popup(self):
        """
        open setting popup
        """
        SettingPopup(self).open()

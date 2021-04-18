from time import sleep

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from libs.backend.local_data_handle import get_readable_time
from libs.backend.custom_exception import DataError
from libs.frontend.chat_widget import UserMessageView, PartnerMessageView
from libs.frontend.custom_popup import ErrorPopup, SettingPopup


class MessageRoute(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.user_profile = self.app.user_profile
        self.authorized_user = None
        self.message_partner = None

    def on_pre_enter(self, *args):
        self.authorized_user = self.app.authorized_user
        self.message_partner = self.app.process_message_partner

        self.ids.message_partner_name.text = \
            self.message_partner.get_username()

        self.display_messages()

    def on_leave(self, *args):
        self.ids.message_scrollview.clear_widgets()
        self.ids.message_content_input.text = ''

    def refresh_messages(self):
        self.ids.message_scrollview.clear_widgets()
        self.display_messages()

    def display_messages(self):
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
        SettingPopup(self).open()

from kivy.uix.screenmanager import Screen

from libs.frontend.chat_widget import UserMessageView, PartnerMessageView
from libs.backend.custom_exception import DataError
from libs.frontend.custom_popup import ErrorPopup


class MessageRoute(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
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

    def display_messages(self):
        try:
            messages = self.authorized_user.get_messages(
                self.message_partner.get_uid()
            )

            for message in messages[::-1]:
                if message.get_senderid() == self.authorized_user.get_uid():
                    self.ids.message_scrollview.add_widget(
                        UserMessageView(message.get_content()))
                else:
                    self.ids.message_scrollview.add_widget(
                        PartnerMessageView(message.get_content()))

        except DataError as error:
            ErrorPopup(error.message).open()

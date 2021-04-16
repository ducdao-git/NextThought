from kivy.uix.boxlayout import BoxLayout

from libs.backend.local_data_handle import get_readable_time


class ChatView(BoxLayout):
    def __init__(self, screen_instance, chat_partner, **kwargs):
        super().__init__(**kwargs)
        self.screen_instance = screen_instance
        self.authorized_user = self.screen_instance.app.authorized_user
        self.chat_partner = chat_partner

        last_message = self.authorized_user.get_messages(
            self.chat_partner.get_uid(), limit=1
        )[0]

        self.ids.chat_partner_name.text = self.chat_partner.get_username()
        self.ids.last_message_preview.text = last_message.get_content()

        self.ids.last_message_time.text = \
            get_readable_time(last_message.get_time())

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and self.collide_point(*touch.opos):
            self.get_messages()

    def get_messages(self):
        print(
            f'get_msg between {self.authorized_user} and {self.chat_partner}')

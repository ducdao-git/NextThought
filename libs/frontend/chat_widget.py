from kivy.uix.boxlayout import BoxLayout


class ChatView(BoxLayout):
    def __init__(self, screen_instance, anon_user, **kwargs):
        super().__init__(**kwargs)
        self.screen_instance = screen_instance
        self.authorized_user = self.screen_instance.app.authorized_user
        self.anon_user = anon_user

        last_message = self.authorized_user.get_messages(
            self.anon_user.get_uid(), limit=1
        )[0].get_content()

        self.ids.last_message_preview.text = \
            self.anon_user.get_username() + '\n' + last_message

    def get_messages(self):
        print(f'get_msg between {self.authorized_user} and {self.anon_user}')

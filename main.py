import kivysome

from kivy.app import App
from kivy.config import Config
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

from libs.backend.local_data_handle import get_theme_palette, UserProfile
from libs.backend.user import AuthorizedUser

from screens.login import LoginRoute
from screens.newsfeed import NewsfeedRoute
from screens.comments import CommentsRoute
from screens.prichat import PriChatRoute
from screens.message import MessageRoute

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '800')

kivysome.enable("https://kit.fontawesome.com/4adb19bb6e.js",
                group=kivysome.FontGroup.SOLID, font_folder="assets/fonts")

Builder.load_file('libs/frontend/custom_kv_widget.kv')
Builder.load_file('libs/frontend/custom_popup.kv')
Builder.load_file('libs/frontend/post_widget.kv')
Builder.load_file('libs/frontend/comment_widget.kv')
Builder.load_file('libs/frontend/chat_widget.kv')
Builder.load_file('screens/login.kv')
Builder.load_file('screens/newsfeed.kv')
Builder.load_file('screens/comments.kv')
Builder.load_file('screens/prichat.kv')
Builder.load_file('screens/message.kv')


class NextMess(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.user_profile = UserProfile()
        self.theme_palette = get_theme_palette('next_mess')

        self.authorized_user = AuthorizedUser('dtuser2', 'ejzifjyt')
        # self.authorized_user = None
        self.process_message_partner = None
        self.process_post = None

        self.route_manager = ScreenManager()

    def build(self):
        """
        call when the app start. it add all screen to screen manager
        """
        self.title = 'NextMess'

        # self.route_manager.add_widget(LoginRoute(app=self))
        self.route_manager.add_widget(NewsfeedRoute(app=self))
        self.route_manager.add_widget(CommentsRoute(app=self))
        self.route_manager.add_widget(PriChatRoute(app=self))
        self.route_manager.add_widget(MessageRoute(app=self))

        self.route_manager.return_route = ''
        return self.route_manager

    def on_stop(self):
        self.user_profile.save_user_profile()


if __name__ == '__main__':
    NextMess().run()

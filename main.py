import kivysome

from kivy.app import App
from kivy.config import Config
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

from libs.local_data_handle import get_theme_palette
from screens.newsfeed import NewsfeedRoute
from libs.authorized_user import AuthorizedUser

# -- delete when done test -- #
from libs.authorized_user import create_user
from libs.public_post import create_public_post

# --------------------------- #

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '800')

kivysome.enable("https://kit.fontawesome.com/4adb19bb6e.js",
                group=kivysome.FontGroup.SOLID, font_folder="assets/fonts")

Builder.load_file('libs/custom_kv_widget.kv')
Builder.load_file('libs/custom_popup.kv')
Builder.load_file('libs/post_widget.kv')
Builder.load_file('screens/newsfeed.kv')


class NextMess(App):
    authorized_user = AuthorizedUser('dtuser2', 'ejzifjyt')
    theme_palette = get_theme_palette('next_mess')
    route_manager = ScreenManager()

    def build(self):
        """
        call when the app start. it add all screen to screen manager
        """
        self.title = 'NextMess'

        self.route_manager.add_widget(NewsfeedRoute(app=self))

        self.route_manager.return_route = ''
        return self.route_manager


if __name__ == '__main__':
    # user2 = AuthorizedUser('dtuser2', 'ejzifjyt')
    # for i in range(4):
    #     create_public_post(user2, f"#test post {i}")

    NextMess().run()

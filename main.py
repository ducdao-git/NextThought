import kivysome

from kivy.app import App
from kivy.config import Config
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

from libs.backend.local_data_handle import get_theme_palette
from libs.backend.authorized_user import AuthorizedUser

from screens.newsfeed import NewsfeedRoute
from screens.comments import CommentsRoute

# -- delete when done test -- #
from libs.backend.public_post import create_public_post, get_public_posts

# --------------------------- #

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '800')

kivysome.enable("https://kit.fontawesome.com/4adb19bb6e.js",
                group=kivysome.FontGroup.SOLID, font_folder="assets/fonts")

Builder.load_file('libs/frontend/custom_kv_widget.kv')
Builder.load_file('libs/frontend/custom_popup.kv')
Builder.load_file('libs/frontend/post_widget.kv')
Builder.load_file('libs/frontend/comment_widget.kv')
Builder.load_file('screens/newsfeed.kv')
Builder.load_file('screens/comments.kv')


class NextMess(App):
    authorized_user = AuthorizedUser('dtuser2', 'ejzifjyt')
    theme_palette = get_theme_palette('next_mess')
    process_post = None
    route_manager = ScreenManager()

    def build(self):
        """
        call when the app start. it add all screen to screen manager
        """
        self.title = 'NextMess'

        self.route_manager.add_widget(NewsfeedRoute(app=self))
        self.route_manager.add_widget(CommentsRoute(app=self))

        self.route_manager.return_route = ''
        return self.route_manager


if __name__ == '__main__':
    # user2 = AuthorizedUser('dtuser2', 'ejzifjyt')
    # create_public_post(user2, 'a'*1000)
    # for i in range(3):
    #     create_public_post(user2, f"#comment {i} parent 94", 99)

    # for pid in [99]:
    #     posts = get_public_posts(uid=5, parent_id=pid)
    #
    #     for post in posts:
    #         post.delete_public_post(user2)

    # create_public_post(user2, 'a'*1000)
    NextMess().run()

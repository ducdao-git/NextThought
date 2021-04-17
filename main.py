import kivysome

from kivy.app import App
from kivy.config import Config
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

from libs.backend.local_data_handle import get_theme_palette
from libs.backend.user import create_user, AuthorizedUser

from screens.newsfeed import NewsfeedRoute
from screens.comments import CommentsRoute
from screens.prichat import PriChatRoute
from screens.message import MessageRoute

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
Builder.load_file('libs/frontend/chat_widget.kv')
Builder.load_file('screens/newsfeed.kv')
Builder.load_file('screens/comments.kv')
Builder.load_file('screens/prichat.kv')
Builder.load_file('screens/message.kv')


class NextMess(App):
    authorized_user = AuthorizedUser('dtuser2', 'ejzifjyt')
    # authorized_user = AuthorizedUser('dtuser4', 'dkhdiznn')
    theme_palette = get_theme_palette('next_mess')
    process_post = None
    process_message_partner = None
    route_manager = ScreenManager()

    def build(self):
        """
        call when the app start. it add all screen to screen manager
        """
        self.title = 'NextMess'

        self.route_manager.add_widget(NewsfeedRoute(app=self))
        self.route_manager.add_widget(CommentsRoute(app=self))
        self.route_manager.add_widget(PriChatRoute(app=self))
        self.route_manager.add_widget(MessageRoute(app=self))

        self.route_manager.return_route = ''
        return self.route_manager


if __name__ == '__main__':
    # user2 = AuthorizedUser('dtuser2', 'ejzifjyt')
    # user3 = AuthorizedUser('dtuser3', 'sphyuddr')
    # user4 = AuthorizedUser('dtuser4', 'dkhdiznn')

    # create_public_post(user2, 'a'*1000)
    # for i in range(3):
    #     create_public_post(user2, f"#comment {i} parent 94", 99)

    # for pid in [99]:
    #     posts = get_public_posts(uid=5, parent_id=pid)
    #
    #     for post in posts:
    #         post.delete_public_post(user2)

    # create_public_post(user2, 'a'*1000)

    # user4.create_message(5, 'hello, this is a msg from user4 to user2')
    # user3.create_message(user2.get_uid(), 'msg 2 from user3 to user2')
    #
    # pprint(user2.get_conversations())
    # pprint(user2.get_messages(user3.get_uid(), limit=1))
    #
    # print('\n')
    # pprint(user3.get_conversations())
    # pprint(user3.get_messages(user2.get_uid(), limit=1))
    NextMess().run()

import kivysome

from kivy.app import App
from kivy.config import Config
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from libs.backend.local_data_handle import get_theme_palette, UserProfile
from libs.backend.response_handle import is_internet_connected

from screens.login import LoginRoute
from screens.newsfeed import NewsfeedRoute
from screens.comments import CommentsRoute
from screens.prichat import PriChatRoute
from screens.message import MessageRoute


class NextMess(App):
    """
    main app class - run if internet connection is good
    """

    def __init__(self, authorized_user=None, goto_route=None, **kwargs):
        """
        initialize some app wide variable like user profile, theme, and screen
        manager.
        :param kwargs: param call for App class
        """
        super().__init__(**kwargs)

        self.user_profile = UserProfile()
        self.theme_palette = \
            get_theme_palette(self.user_profile.get_theme_name())

        self.authorized_user = authorized_user
        self.process_message_partner = None
        self.process_post = None
        self.goto_route = goto_route

        self.route_manager = None

    def build(self):
        """
        call when the app start. it set the app name add all screen to screen
        manager.
        """
        self.title = 'NextMess'

        self.route_manager = None

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

        self.route_manager = ScreenManager()

        self.route_manager.add_widget(LoginRoute(app=self))
        self.route_manager.add_widget(NewsfeedRoute(app=self))
        self.route_manager.add_widget(CommentsRoute(app=self))
        self.route_manager.add_widget(PriChatRoute(app=self))
        self.route_manager.add_widget(MessageRoute(app=self))

        self.route_manager.return_route = ''

        if self.goto_route is not None:
            self.route_manager.current = self.goto_route

        return self.route_manager

    def refresh_theme(self):
        """
        call when change theme. by create a new app instance, all new theme
        will be load in. costly but this is the only method not cause conflict
        when clear widget
        """
        Builder.unload_file('libs/frontend/custom_kv_widget.kv')
        Builder.unload_file('libs/frontend/custom_popup.kv')
        Builder.unload_file('libs/frontend/post_widget.kv')
        Builder.unload_file('libs/frontend/comment_widget.kv')
        Builder.unload_file('libs/frontend/chat_widget.kv')
        Builder.unload_file('screens/login.kv')
        Builder.unload_file('screens/newsfeed.kv')
        Builder.unload_file('screens/comments.kv')
        Builder.unload_file('screens/prichat.kv')
        Builder.unload_file('screens/message.kv')
        
        self.build()

    def on_stop(self):
        """
        save user profile locally on app stop
        """
        self.user_profile.save_user_profile()


class AppCrashScreen(Screen):
    """
    screen display if unable to run app at all
    """
    pass


class NextMessCrash(App):
    """
    run this 'app' version if unable to run the main app
    """

    def __init__(self, **kwargs):
        """
        initialize app wide variable theme
        :param kwargs: param call for App class
        """
        super().__init__(**kwargs)
        self.user_profile = UserProfile()
        self.theme_palette = \
            get_theme_palette(self.user_profile.get_theme_name())

    def build(self):
        """
        call when the main app unable to start. it set the app name and display
        the crash screen
        """
        self.title = 'NextMess'
        return AppCrashScreen()


if __name__ == '__main__':
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '800')

    # if no internet then open the crash version of the app. do this because
    # the icon fonts require internet connection to load thus the main app
    # cannot run if no internet connection.
    if not is_internet_connected():
        Builder.load_file('screens/app_crash.kv')
        NextMessCrash().run()

    else:
        kivysome.enable("https://kit.fontawesome.com/4adb19bb6e.js",
                        group=kivysome.FontGroup.SOLID,
                        font_folder="assets/fonts")

        NextMess().run()

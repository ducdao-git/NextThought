from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from libs.backend.local_data_handle import get_readable_time
from libs.backend.custom_exception import DataError
from libs.frontend.custom_kv_widget import IconButton
from libs.frontend.custom_popup import OneInputFieldPopup, ErrorPopup


class PostInfoButton(Button):
    def __init__(self, owner_name, posted_time, **kwargs):
        super().__init__(**kwargs)
        self.text = f"[b]{owner_name}[/b]\n[size=12sp][color=" \
                    f"{self.posted_time_color}]{posted_time}[/color][/size]"

        self.bind(size=self.update_text_size)
        self.bind(texture_size=self.update_height)

    def update_text_size(self, *args):
        """
        update value of text_size. this function make sure the text_size not
        take widget default/initial size as the value
        """
        self.text_size = self.width, None

    def update_height(self, *args):
        """
        update value of widget height. this function make sure the height not
        take widget default/initial texture_size as the value
        """
        self.height = self.texture_size[1]


class PostContentButton(Button):
    def __init__(self, post_content, **kwargs):
        super().__init__(**kwargs)
        self.text = post_content

        self.bind(size=self.update_text_size)
        self.bind(texture_size=self.update_height)

    def update_text_size(self, *args):
        """
        update value of text_size. this function make sure the text_size not
        take widget default/initial size as the value
        """
        self.text_size = self.width, None

    def update_height(self, *args):
        """
        update value of widget height. this function make sure the height not
        take widget default/initial texture_size as the value
        """
        self.height = self.texture_size[1]


class PostDividerLabel(Label):
    """
    custom label with height 1 to act as divider
    """

    def __init__(self, **kwargs):
        """
        create a label to act as a divider
        """
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(rgba=self.color)
            self.rect = Rectangle()

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        """
        update position and size of rectangle in the canvas instruction. this
        function make sure canvas not take widget default position and size
        """
        self.rect.pos = self.pos
        self.rect.size = self.size


class PostOptionButton(IconButton):
    def __init__(self, view_instance, option_action, **kwargs):
        super().__init__(**kwargs)
        self.option_action = option_action
        self.view_instance = view_instance

        if option_action == 'edit':
            option_icon = self.edit_icon
        elif option_action == 'delete':
            option_icon = self.delete_icon
        else:
            option_icon = self.error_icon

        self.text = f'[size=16sp]{option_icon}[/size]'

    def on_release(self):
        if self.option_action == 'edit':
            return self.view_instance.get_post_new_content()
        elif self.option_action == 'delete':
            return self.view_instance.post_delete()
        else:
            return None


class PostActionBar(BoxLayout):
    def __init__(self, view_instance, **kwargs):
        super().__init__(**kwargs)
        self.view_instance = view_instance

        self.ids.post_section_divider_holder.add_widget(
            PostDividerLabel(height=dp(1)))

        self.upvotes_num = self.view_instance.post.get_upvotes_num()
        self.display_post_upvotes()

        self.comments_num = self.view_instance.post.get_comments_num()
        self.display_post_comments_num()

        self.bind(minimum_height=self.setter('height'))

    def display_post_upvotes(self):
        if self.upvotes_num != 0:
            upvote_text = str(self.upvotes_num)
        else:
            upvote_text = 'Like'

        self.ids.post_like_button.text = \
            self.heart_icon + f' [size=12sp]{upvote_text}[/size]'

    def display_post_comments_num(self):
        if self.comments_num != 0:
            comment_btn_text = str(self.comments_num)
        else:
            comment_btn_text = 'Comment'

        self.ids.post_comment_button.text = \
            self.comment_icon + f' [size=12sp]{comment_btn_text}[/size]'

    def upvote_post(self):
        curr_post = self.view_instance.post
        curr_user = self.view_instance.screen_instance.app.authorized_user
        try:
            curr_post.upvote_post(curr_user)

            self.upvotes_num += 1
            self.ids.post_like_button.text = \
                self.heart_icon + \
                f' [size=12sp]{self.upvotes_num}[/size]'

        except DataError as error:
            ErrorPopup(error.message).open()


class PostView(BoxLayout):
    """
    custom boxlayout to display a public post
    """

    def __init__(self, screen_instance, post, **kwargs):
        super().__init__(**kwargs)
        self.screen_instance = screen_instance
        self.post = post
        # self.post_new_content = 'edit -- sth go wrong'

        self.ids.row.add_widget(
            PostInfoButton(self.post.get_owner_name(),
                           get_readable_time(self.post.get_time()))
        )

        if self.screen_instance.app.authorized_user.get_username() == \
                self.post.get_owner_name():
            self.ids.row.add_widget(PostOptionButton(self, 'edit'))
            self.ids.row.add_widget(PostOptionButton(self, 'delete'))

        self.add_widget(PostContentButton(self.post.get_content()))

        self.add_widget(PostActionBar(self))
        self.add_widget(PostDividerLabel(height=dp(10)))

        self.bind(minimum_height=self.setter('height'))

    def get_post_new_content(self):
        OneInputFieldPopup(view_instance=self, action_name='edit_post').open()

    def post_edit(self, post_new_content):
        if post_new_content == '':
            return

        try:
            self.post.edit_public_post(
                self.screen_instance.app.authorized_user,
                post_new_content
            )

            # self.post_new_content = post_new_content
            self.screen_instance.refresh_newsfeed()

        except DataError as error:
            ErrorPopup(error.message).open()

    def post_delete(self):
        try:
            self.post.delete_public_post(
                self.screen_instance.app.authorized_user
            )
            self.screen_instance.ids.newsfeed_scrollview.remove_widget(self)
        except DataError as error:
            ErrorPopup(error.message).open()

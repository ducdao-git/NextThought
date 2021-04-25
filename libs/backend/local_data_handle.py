import json
from datetime import datetime, timedelta
from dateutil import tz

from libs.backend.custom_exception import DataError


def _hex_to_rgb(hex_color):
    """
    :param hex_color: valid hex code of a color
    :return: rgba value each between 0 and 1
    """
    hex_color = hex_color.lstrip('#')
    hex_color = list(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    result = []
    for value in hex_color:
        result.append(round(value / 255, 3))

    result.append(1.0)

    return result


def get_theme_palette(theme_name):
    """
    get color data of the theme_name
    :param theme_name: string repr name of the theme
    :return: color palette for the theme
    """
    try:
        if theme_name not in ['light', 'dark']:
            raise ValueError

        with open('assets/theme_palettes.json', 'r') as f:
            themes_data = json.load(f)

        theme_data = themes_data[theme_name]
        theme_palette = {}

        for color in theme_data:
            if color in ['support_text_color', 'good_color']:
                theme_palette[color] = theme_data[color]
            else:
                theme_palette[color] = _hex_to_rgb(theme_data[color])

        # pprint(theme_palette)
        return theme_palette

    except Exception as error:
        raise DataError(error)


def get_readable_time(time, message_time=False):
    """
    get human easy readable time, the time format will vary depend on how long
    was it from current time and if it is message time or not. message display
    time have different format from post or comment display time. if unable to
    convert utc time to local time, raise DataError.
    :param time: string repr the time of post, comment, or message
    :param message_time: boolean to check if the time is message time
    :return: string repr readable form of the time
    """
    try:
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        post_utc_time = datetime.strptime(
            time, '%Y-%m-%d %H:%M:%S'
        ).replace(tzinfo=from_zone)

        post_local_time = post_utc_time.astimezone(to_zone)
        curr_time = datetime.now().astimezone(to_zone)
        time_diff = curr_time - post_local_time

        if message_time:
            if (time_diff / timedelta(days=365)) > 1:
                return post_local_time.strftime('%b %d, %Y AT %H:%M')
            else:
                return post_local_time.strftime('%b %d AT %H:%M')

        elif (time_diff / timedelta(days=365)) > 1:
            return post_local_time.strftime('%x')
        elif (time_diff / timedelta(days=1)) > 1:
            return post_local_time.strftime('%b %d')
        elif (time_diff / timedelta(hours=1)) > 1:
            return str(time_diff.seconds // 3600) + 'h'
        elif (time_diff / timedelta(minutes=1)) > 1:
            return str(time_diff.seconds // 60) + 'm'
        else:
            return str(time_diff.seconds) + 's'

    except Exception as error:
        print(f'error ppost get_time: {error}')
        raise DataError(error)


class UserProfile:
    """
    class repr a user profile
    """

    def __init__(self):
        """
        create a UserProfile obj from user_profile local file save. if unable
        to read local file save, raise DataError
        """
        try:
            with open('user_profile.json', 'r') as infile:
                self.user_profile = json.load(infile)

            # pprint(self.user_profile)

        except Exception as error:
            raise DataError(error)

    def get_theme_name(self):
        """
        :return: string repr name of the theme user are currently use
        """
        return self.user_profile['theme_name']

    def get_do_save_auth(self):
        """
        :return: 1 or 0, where 1 mean do save auth, 0 mean don't save auth
        """
        return self.user_profile['do_save_auth']

    def get_saved_username(self):
        """
        :return: string repr saved username
        """
        return self.user_profile['saved_username']

    def get_saved_token(self):
        """
        :return: string repr saved token
        """
        return self.user_profile['saved_token']

    def get_num_post_show(self):
        """
        :return: string repr maximum post will be show
        """
        return self.user_profile['num_post_show']

    def get_num_message_show(self):
        """
        :return: string repr maximum message will be show
        """
        return self.user_profile['num_message_show']

    def set_theme_name(self, new_theme_name):
        """
        set new value for theme_name. raise DataError if new_theme_name neither
        'light' nor 'dark'
        :param new_theme_name: string repr name of the new theme
        """
        if new_theme_name not in ['light', 'dark']:
            raise DataError('Invalid theme name')

        self.user_profile['theme_name'] = new_theme_name

    def switch_do_save_auth(self, switch_to_state):
        """
        change value of do_save_auth. do_save_auth can only take 1 or 0. Where
        1 mean do save auth, 0 mean don't save auth
        :param switch_to_state: boolean repr do_save_auth equal to this state
        """
        if switch_to_state:
            self.user_profile['do_save_auth'] = 1
        else:
            self.user_profile['do_save_auth'] = 0

    def set_saved_username(self, new_saved_username):
        """
        set value for saved_username
        :param new_saved_username: string repr new username to be save
        """
        self.user_profile['saved_username'] = new_saved_username

    def set_saved_token(self, new_saved_token):
        """
        set value for saved_token
        :param new_saved_token: string repr new token to be save
        """
        self.user_profile['saved_token'] = new_saved_token

    def set_num_post_show(self, new_num_post_show):
        """
        set value for num_post_show. the value must be in 1 to 100 inclusively,
        else raise raise DataError
        :param new_num_post_show: int repr new maximum number of post will be
        show
        """
        if new_num_post_show.isdigit():
            new_num_post_show = int(new_num_post_show)
        else:
            raise DataError('Number of Post Show must be integer')

        if new_num_post_show < 1:
            raise DataError('Number of Post Show must be a positive'
                            ' integer (number > 0)')
        elif new_num_post_show > 100:
            raise DataError(
                'Number of Post Show cannot excess 100 (number < 101)'
            )

        self.user_profile['num_post_show'] = new_num_post_show

    def set_num_message_show(self, new_num_message_show):
        """
        set value for num_message_show. the value must be in 1 to 100
        inclusively, else raise raise DataError
        :param new_num_message_show: int repr new maximum number of message
        will be show
        """
        if new_num_message_show.isdigit():
            new_num_message_show = int(new_num_message_show)
        else:
            raise DataError('Number of Message Show must be integer')

        if new_num_message_show < 1:
            raise DataError('Number of Message Show must be a positive'
                            ' integer (number > 0)')
        elif new_num_message_show > 100:
            raise DataError(
                'Number of Message Show cannot excess 100 (number < 101)'
            )

        self.user_profile['num_message_show'] = new_num_message_show

    def save_user_profile(self):
        """
        save user profile to local user_profile file to preserve setting. if
        unable to write to local user_profile file, raise DataError
        """
        try:
            with open('user_profile.json', 'w') as outfile:
                json.dump(self.user_profile, outfile, indent=2)
        except Exception as error:
            raise DataError(error)

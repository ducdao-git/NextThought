import json
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
    :param theme_name: name of the theme - next_mess
    :return: color palette for the theme
    """
    try:
        if theme_name not in ['next_mess', 'dark']:
            raise ValueError

        with open('assets/theme_palettes.json', 'r') as f:
            themes_data = json.load(f)

        theme_data = themes_data[theme_name]
        theme_palette = {}

        for color in theme_data:
            if color in ['support_text_color']:
                theme_palette[color] = theme_data[color]
            else:
                theme_palette[color] = _hex_to_rgb(theme_data[color])

        # pprint(theme_palette)
        return theme_palette

    except Exception as error:
        raise DataError(error)

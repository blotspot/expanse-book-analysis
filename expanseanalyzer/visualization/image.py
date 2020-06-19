from PIL import Image, ImageDraw, ImageFont, ImageColor

from expanseanalyzer.common.constants import EXTERNAL_DATA_DIR

FONT = str(EXTERNAL_DATA_DIR / 'Protomolecule-Black.ttf')
MARGIN = 0.05

BOOK_COLORS = {
    "Leviathan Wakes": '#2B678C',
    "Caliban's War": '#1D1440',
    "Abbadon's Gate": '#590E0E',
    "Cibola Burn": '#2D7337',
    "Nemesis Games": '#F22233',
    "Babylon's Ashes": '#05C7F2',
    "Persepolis Rising": '#8C6316',
    "Tiamaths Wrath": '#F24822'
}


def text_to_image(book_title: str, text: str, font_size: int) -> Image:
    """
    Generates an image from the given text.

    :param book_title: title of the book, defines color
    :param text: text to display in image
    :param font_size: size of the text
    :return: generated image
    """
    text = text.upper()
    font = ImageFont.truetype(FONT, font_size)
    return _text_to_image(text, font, ImageColor.getrgb('#FFF'), ImageColor.getrgb(BOOK_COLORS[book_title]))


def _text_to_image(text, font, background_color, text_color, condensation_factor=0.1):
    """
    Produces an image that contains the given text in the given font,
    with the spacing between the letters being condensed by the given condensation factor.

    :param text: Text to draw on the image.
    :param font: Font to draw the text with.
    :param background_color: color tuple.
    :param text_color: color tuple.
    :param condensation_factor: (0 - 1) 0: no condensation of the letters. 1: all letters will be drawn over each other.
    :return: Image with the specified text drawn into it.
       The width and height of the produced image will depend on the given font and condensation_factor
    """
    condensation_factor = min(1.0, max(0.0, condensation_factor))
    word_size = font.getsize(text)
    condensation_value = int(word_size[1] * condensation_factor)
    img = Image.new('RGB', word_size, background_color)
    draw = ImageDraw.Draw(img)
    space = int(word_size[1] * 0.1)
    cur_x = 0
    static_y = 0 - space
    for letter in text:
        letter_size = font.getsize(letter)
        draw.text((cur_x, static_y), letter, fill=text_color, font=font)
        cur_x = cur_x + max(letter_size[0] - condensation_value, 0)
    img = img.crop((0, 0, cur_x + condensation_value, word_size[1]))

    return img

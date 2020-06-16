import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
from matplotlib import rcParams
from wordcloud import WordCloud, ImageColorGenerator

from src.common import constants
from src.nlp.util import STOPWORDS
from src.visualization.image import text_to_image


plt.style.use(constants.EXTERNAL_DATA_DIR / "mpl/expanse.mplstyle")

DEFAULT_COLOR = '#333F4B'
DEFAULT_LINE_WIDTH = 0.5

WIDTH = 170 * constants.MM_TO_INCH
HEIGHT = WIDTH / constants.PHI

# rcParams['figure.figsize'] = (WIDTH, HEIGHT)
# rcParams['figure.dpi'] = 180


def scatter_plot(num: int, book: str, file_prefix: str, x_axis: tuple, y_axis: tuple, col_bar: tuple):
    """
    Plots a scatter diagram.

    :param num: book number (for file naming only)
    :param book: book title (figure title and file name)
    :param file_prefix: custom text before number and title in filename
    :param x_axis: tuple of x-axis title and values
    :param y_axis: tuple of y-axis title and values
    :param col_bar: tuple of colorbar title and values
    """
    x_label, x_values = x_axis
    y_label, y_values = y_axis
    c_label, c_values = col_bar
    scatter_plt = plt.scatter(x=x_values, y=y_values, s=500, alpha=0.55,
                              c=c_values, cmap=cm.get_cmap('viridis', 10), vmin=0, vmax=1,
                              clip_on=False,
                              linewidth=1)

    # add labels to data points
    for label, x_val, y_val in zip(labels, x_values, y_values):
        plt.annotate(label,
                     (x_val, y_val),
                     textcoords='offset points',
                     xytext=(0, 0),
                     ha='center',
                     va='center',
                     size=5,
                     weight='medium',
                     color=DEFAULT_COLOR)

    color_bar = plt.colorbar(scatter_plt)
    color_bar.outline.set_visible(False)
    color_bar.outline.set_linewidth(DEFAULT_LINE_WIDTH)
    color_bar.ax.set_ylabel(c_label, rotation=270, labelpad=24)
    color_bar.ax.tick_params(direction='inout', width=DEFAULT_LINE_WIDTH, length=0)
    color_bar.ax.spines['right'].set_visible(True)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(label_book(book), color=DEFAULT_COLOR)

    # Additional Axis styling.
    plt.scatter([0, 1], [0, 1], s=0)
    axis = plt.gca()
    axis.set_xlim([-0.02 / constants.PHI, 1.0000000001])
    axis.set_ylim([-0.02, 1.0000000001])
    axis.spines['top'].set_color('none')
    axis.spines['right'].set_color('none')
    axis.spines['left'].set_bounds(0, 1)
    axis.spines['bottom'].set_bounds(0, 1)
    axis.set_axisbelow(True)
    axis.yaxis.grid(True)
    axis.xaxis.grid(True)
    axis.tick_params(width=DEFAULT_LINE_WIDTH)

    # save as png
    plt.savefig(constants.REPORTS_DIR / 'figures' / '{} {} {}.png'.format(file_prefix, num, book))
    plt.close()


def grouped_bar_plot(first: tuple, second: tuple, axis):
    """
    Plots a grouped bar diagram.

    :param first: tuple with bar name and list of values for first bar
    :param second: tuple with bar name and list of values for second bar
    :param axis axis object
    """
    first_title, first_data = first
    second_title, second_data = second

    x = np.arange(len(labels))
    bar_width = 0.4
    # style_axis(False)
    axis.bar(x, first_data, width=bar_width, label=first_title, color='#d1a94d')
    axis.bar(x + bar_width, second_data, width=bar_width, label=second_title, color='#4c7648', alpha=1)
    axis.legend()
    axis.set_xticks(x + bar_width / 2)
    axis.set_xticklabels(labels, rotation=45, ha="right")

    # Axis styling.
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['left'].set_visible(False)
    axis.spines['bottom'].set_color(DEFAULT_COLOR)
    axis.tick_params(bottom=False, left=False, width=DEFAULT_LINE_WIDTH)
    axis.set_axisbelow(True)
    axis.yaxis.grid(True)
    axis.xaxis.grid(False)


def plot_grouped_bars(num: int, book: str, figure_title: str, first: tuple, second: tuple):
    """
    Plots a grouped bar chart
    :param num: book number (for file naming only)
    :param book: book title (figure title and file name)
    :param figure_title: figure title
    :param first: tuple with bar name and list of values for first bar
    :param second: tuple with bar name and list of values for second bar
    """
    plt.figure()
    axis = plt.gca()

    axis.title.set_text('{} // {}'.format(figure_title, label_book(book)))

    grouped_bar_plot(first, second, axis)
    # save as png
    plt.savefig(constants.REPORTS_DIR / 'figures' / '{} {} {}.png'.format(figure_title, num, book))
    plt.close()


def label_book(book_title):
    """
    converts the book title into an 'expansish' label (replace upper- with lowercase and use "_" instead of whitespace)
    :param book_title: book title
    :return: formatted book title
    """
    return ''.join(char.lower() if char.isupper() else char.upper() for char in book_title).replace(' ', '_')


def word_cloud(num, book_title):
    """
    Generates a word cloud for each character that has its own chapter in the book.

    :param num: book number
    :param book_title: book title
    """
    from src.common import load_book

    book = load_book(book_title)
    pov_characters = {pov.ref_name for pov in book.pov_characters()}
    for pov in pov_characters:
        LOGGER.info('Generate wordcloud for %s ...', pov)
        words = ' '.join([chapter.content() for chapter in book.chapters_by_pov(pov)])
        stopwords_exclude_own_name = STOPWORDS.copy()
        stopwords_exclude_own_name.add(pov)
        img = text_to_image(book_title, pov, 650)
        wc_mask = np.array(img)
        cloud = WordCloud(
            width=img.size[0],
            height=img.size[1],
            stopwords=stopwords_exclude_own_name,
            regexp=r'(?!-)(?:-\b|\b-|\w)+(?=\b)',
            background_color='white',
            min_font_size=10,
            max_words=1000,
            mask=wc_mask,
            font_path=constants.WORD_CLOUD_FONT_PATH,
            collocations=False
        )
        cloud = cloud.generate(words)
        image_colors = ImageColorGenerator(wc_mask)
        cloud = cloud.recolor(color_func=image_colors)
        cloud.to_file(constants.REPORTS_DIR / 'figures' / 'Wordcloud {} {} - {}.png'.format(num, book_title, pov))


if __name__ == "__main__":
    from src.common import load_book_titles

    # For this to work we need to run 'make_dataset.py' first
    logging.basicConfig(level=logging.INFO, format=constants.LOGGER_FORMAT)
    LOGGER = logging.getLogger(__name__)

    for i, title in enumerate(load_book_titles()):
        book_nr = i + 1
        df = pd.read_csv(constants.PROCESSED_DATA_DIR / constants.CENTRALITY_CSV_FILENAME.format(title), header=0)
        # sort by mentions and take only most mentioned characters
        df = df.sort_values(by=constants.CSV_CHAR_MENT, ascending=False).head(15)

        # Format labels as uppercase for readability
        labels = [l.upper() for l in df.label]

        LOGGER.info('Plot figures for %s ...', title)
        scatter_plot(book_nr, title, 'Fractal',
                     ('ImportancE (pAgErAnk)', df[constants.CENT_CSV_TR].to_numpy()),
                     # Importance of a Character in the Network
                     ('InfluencE (Katz)', df[constants.CENT_CSV_KATZ].to_numpy()),
                     # Influence of a Character in the Network
                     ('intEractions (DEEGre)', df[constants.CENT_CSV_DEG].to_numpy()))

        # Compare NetworkX Text(Page)Rank results vs. my implementation
        plot_grouped_bars(
            book_nr, title, 'tExtrAnk',
            ('NEtworkX', df[constants.CENT_CSV_TR].to_numpy()),
            ('My ImplEmEntation', df[constants.CENT_CSV_OTR].to_numpy())
        )
        # Compare NetworkX Eigenvector results vs. my implementation
        plot_grouped_bars(
            book_nr, title, 'EigenvEctor',
            ('NEtworkX', df[constants.CENT_CSV_EV].to_numpy()),
            ('My ImplEmEntation', df[constants.CENT_CSV_OEV].to_numpy())
        )

        # Compare NetworkX Eigenvector results vs. Katy Centrality results
        plot_grouped_bars(
            book_nr, title, 'Katz vs EV',
            ('EigenvEctor', df[constants.CENT_CSV_EV].to_numpy()),
            ('Katz CEntrality', df[constants.CENT_CSV_KATZ].to_numpy())
        )

        # word_cloud(book_nr, title)

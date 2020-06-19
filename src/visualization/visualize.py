import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator

from src.common import constants
from src.nlp.util import STOPWORDS
from src.visualization.color import expanse_cmap, expanse_colors
from src.visualization.image import text_to_image

plt.style.use(constants.EXTERNAL_DATA_DIR / "mpl/expanse.mplstyle")
# WIDTH = 170 * constants.MM_TO_INCH
# HEIGHT = WIDTH / constants.PHI


def scatter_plot(num: int, book: str, x_axis: tuple, y_axis: tuple, col_bar: tuple):
    """
    Plots a scatter diagram.

    :param num: book number (for file naming only)
    :param book: book title (figure title and file name)
    :param x_axis: tuple(title, values) for x-axis
    :param y_axis: tuple(title, values) for y-axis
    :param col_bar: tuple(title, values) for color bar
    """
    scatter_plt = plt.scatter(x=x_axis[1], y=y_axis[1], s=500, alpha=0.55,
                              c=col_bar[1], cmap=expanse_cmap(n=10, mode='hls'), vmin=0, vmax=1,
                              clip_on=False,
                              linewidth=1)

    # add labels to data points
    for label, x_val, y_val in zip(labels, x_axis[1], y_axis[1]):
        plt.annotate(label,
                     (x_val, y_val),
                     textcoords='offset points',
                     xytext=(0, 0),
                     ha='center', va='center',
                     size=5, weight='medium')

    color_bar = plt.colorbar(scatter_plt)
    color_bar.outline.set_visible(False)
    color_bar.ax.set_ylabel(col_bar[0], rotation=270, labelpad=24)
    color_bar.ax.tick_params(length=0)

    plt.xlabel(x_axis[0])
    plt.ylabel(y_axis[0])
    plt.title(label_book(book))

    # Additional styling
    plt.scatter(x=[0, 1], y=[0, 1], s=0)  # s=0 prevents that strange dots appear at 0,0 and 1,1
    axis = plt.gca()  # get axis object for decoupled x and y axis line stroke effect
    axis.set_xlim([-0.02 / constants.PHI, 1.0000000001])  # make the axis limitations a bit higher than the data range
    axis.set_ylim([-0.02, 1.0000000001])    # this basically creates a padding between the data and the line strokes
    axis.spines['left'].set_bounds(0, 1)    # make sure spines are still in data range to make the line strokes appear
    axis.spines['bottom'].set_bounds(0, 1)  # to be decoupled

    save(num, book, 'fractal')


def grouped_bar_plot(first: tuple, second: tuple, axis):
    """
    Plots a grouped bar diagram.

    :param first: tuple with bar name and list of values for first bar
    :param second: tuple with bar name and list of values for second bar
    :param axis: axis object
    """
    first_title, first_data = first
    second_title, second_data = second

    x = np.arange(len(labels))
    bar_width = 0.4
    colors = expanse_colors(2)
    axis.bar(x, first_data, width=bar_width, label=first_title, color=colors[0], alpha=0.65)
    axis.bar(x + bar_width, second_data, width=bar_width, label=second_title, color=colors[1], alpha=0.65)
    axis.set_xticks(x + bar_width / 2)
    axis.set_xticklabels(labels, rotation=45, ha="right")
    # additional styling
    axis.tick_params(bottom=False, left=False)  # No ticks left and bottom
    axis.spines['left'].set_visible(False)  # No line on the left
    axis.xaxis.grid(False)  # No vertical grid lines
    axis.legend()


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
    save(num, book, figure_title)


def save(book_num: int, book_title: str, suffix: str):
    """
    Saves a mpl figure as png in the reports folder under the name:
    "{book_num} {book_title} {suffix}.png"

    Leviathan Wakes would therefore produce: "01 Leviathan Wakes fractal.png"

    :param book_num: book number
    :param book_title: book title
    :param suffix:
    """
    # save as png
    plt.savefig(constants.REPORTS_DIR / 'figures' / '{0:02d} {1} {2}.png'.format(book_num, book_title, suffix.lower()))
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
        img = text_to_image(book_title, pov, 650)  # make an image out of the characters name
        wc_mask = np.array(img)
        cld = WordCloud(
            width=img.size[0],
            height=img.size[1],
            stopwords=stopwords_exclude_own_name,
            regexp=r'(?!-)(?:-\b|\b-|\w)+(?=\b)',
            background_color='white',
            min_font_size=10,
            max_words=1000,
            mask=wc_mask,
            font_path=constants.WORD_CLOUD_FONT_PATH,  # Load 'Protomolecule Black' Font
            collocations=False
        )
        cld = cld.generate(words)
        image_colors = ImageColorGenerator(wc_mask)
        cld = cld.recolor(color_func=image_colors)
        cld.to_file(constants.REPORTS_DIR / 'figures' / '{0:02d} {1} wordcloud - {2}.png'.format(num, book_title, pov))


if __name__ == "__main__":
    from src.common import load_book_titles

    logging.basicConfig(level=logging.INFO, format=constants.LOGGER_FORMAT)
    LOGGER = logging.getLogger(__name__)

    for i, title in enumerate(load_book_titles()):
        book_nr = i + 1
        # load character centralities for the book
        df = pd.read_csv(constants.PROCESSED_DATA_DIR / constants.CENTRALITY_CSV_FILENAME.format(title), header=0)
        # sort by mentions and take only most mentioned characters
        df = df.sort_values(by=constants.CSV_CHAR_MENT, ascending=False).head(15)

        # Format labels as uppercase for readability
        labels = [label.upper() for label in df.label]

        LOGGER.info('Plot figures for %s ...', title)
        scatter_plot(book_nr, title,
                     ('ImportancE (pAgErAnk)', df[constants.CENT_CSV_TR].to_numpy()),
                     ('InfluencE (Katz)', df[constants.CENT_CSV_KATZ].to_numpy()),
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

        word_cloud(book_nr, title)

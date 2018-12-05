"""
Shows a result of the report. Prints into console top 5 authors/articles
and shows a bar chart with matplotlib
"""
from matplotlib import pyplot as plt
import pandas as pd
import logging

logger = logging.getLogger('report.visualizer')
_top_tags_count = 7
_top_authors_count = 5
_top_articles_count = 5


def visualize(_authors, _articles):
    """
    Main method to show results
    :param _authors: all authors to process
    :param _articles: all articles to process
    :return: void
    """
    top_authors, top_articles = get_top_authors_articles(_authors, _articles)
    print_top_authors_articles(top_authors, top_articles)
    top_tag_count, top_tags = collect_top_tags(_articles)
    show_plot(top_tag_count, top_tags)


def show_plot(top_tag_count, top_tags):
    """
    Shows a horizontal bar char with tags and their count
    :param top_tag_count: list of tag's count
    :param top_tags: list of related tags
    :return: void
    """
    df = pd.DataFrame({
        'count': top_tag_count,
        'tag': top_tags
    })
    df.plot.barh(x='tag', y='count', rot=0, title='Tags count', figsize=(10, 4))
    plt.tight_layout()
    plt.show()


def collect_top_tags(_articles):
    """
    Calculates most used tags
    :param _articles: list of articles
    :return: lists of tag's count and related tags
    """
    tags = {}
    for article in _articles:
        for tag in article['tags']:
            if tag in tags:
                tags[tag] = tags[tag] + 1
            else:
                tags[tag] = 1
    sorted_tags = sorted(tags, key=lambda k: tags[k])
    top_tags = sorted_tags[-_top_tags_count:]
    top_tag_count = []
    for tag in top_tags:
        top_tag_count.append(tags[tag])
    return top_tag_count, top_tags


def get_top_authors_articles(_authors, _articles):
    """
    Sorts and returns top 5 authors by posts count
    and 5 articles by date
    :param _authors:
    :param _articles:
    :return:
    """
    _authors.sort(reverse=True, key=lambda k: k['posts'])
    _articles.sort(reverse=True, key=lambda k: k['date'])
    top_authors = _authors[:_top_authors_count]
    top_articles = _articles[:_top_articles_count]
    return top_authors, top_articles


def print_top_authors_articles(top_authors, top_articles):
    """
    Prints into console data about top authors/articles
    :param top_authors: list
    :param top_articles: list
    :return: void
    """
    logger.info('top authors:')
    for index, author in enumerate(top_authors):
        print(f"{str(index + 1)}. {author['name']} - {author['posts']}")

    logger.info('top new articles:')
    for index, article in enumerate(top_articles):
        print(f"{str(index + 1)}. {article['title']}")


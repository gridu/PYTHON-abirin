from matplotlib import pyplot as plt
import pandas as pd
import logging

logger = logging.getLogger('report.visualizer')


def visualize(_authors, _articles):
    top_authors, top_articles = get_top_authors_articles(_authors, _articles)
    print_top_authors_articles(top_authors, top_articles)
    top_tag_count, top_tags = collect_top_tags(_articles)
    show_plot(top_tag_count, top_tags)


def show_plot(top_tag_count, top_tags):
    df = pd.DataFrame({
        'count': top_tag_count,
        'tag': top_tags
    })
    df.plot.barh(x='tag', y='count', rot=0, title='Tags count', figsize=(10, 4))
    plt.tight_layout()
    plt.show()


def collect_top_tags(_articles):
    tags = {}
    for article in _articles:
        for tag in article['tags']:
            if tag in tags:
                tags[tag] = tags[tag] + 1
            else:
                tags[tag] = 1
    sorted_tags = sorted(tags, key=lambda k: tags[k])
    top_tags = sorted_tags[-7:]
    top_tag_count = []
    for tag in top_tags:
        top_tag_count.append(tags[tag])
    return top_tag_count, top_tags


def get_top_authors_articles(_authors, _articles):
    _authors.sort(reverse=True, key=lambda k: k['posts'])
    _articles.sort(reverse=True, key=lambda k: k['date'])
    top_authors = _authors[:5]
    top_articles = _articles[:5]
    return top_authors, top_articles


def print_top_authors_articles(top_authors, top_articles):
    logger.info('top authors:')
    for index, author in enumerate(top_authors):
        print(f"{str(index + 1)}. {author['name']} - {author['posts']}")

    logger.info('top new articles:')
    for index, article in enumerate(top_articles):
        print(f"{str(index + 1)}. {article['title']}")


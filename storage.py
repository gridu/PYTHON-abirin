"""
This is json storage manager
"""
import json
import os.path
from datetime import datetime
import logging

storage_name = 'articles.txt'
logger = logging.getLogger('report.storage')


def change_storage(file_name):
    """
    Changes the storage location
    :param file_name: new name of the json storage file
    :return: void
    """
    global storage_name
    storage_name = file_name


def get(_authors, _articles):
    """
    Reads storage file, adds only new items from method input and returns everything
    :param _authors: list of scrapped authors from website
    :param _articles: list of scrapped articles from website
    :return: tuple of authors, articles combined from new and stored in the storage
    """
    authors, articles = read()
    if not articles:
        logger.info('first launch: storage is empty')
        return _authors, _articles

    last_stored_article = articles[-1]
    last_date = last_stored_article['date']
    last_date_formatted = datetime.utcfromtimestamp(last_date).strftime("%d-%m-%Y")
    logger.info("last stored article's date:" + last_date_formatted)

    index = 0
    new_articles = []
    while index < len(_articles):
        article = _articles[index]
        if article['date'] > last_date:
            new_articles.append(article)
        index += 1

    if not new_articles:
        logger.info('no new articles')
        return authors, articles

    new_authors = []
    for author in _authors:
        if author not in authors:
            new_authors.append(author)

    logger.info(str(len(new_articles)) + ' new articles')
    logger.info(str(len(new_authors)) + ' new authors')
    return authors + new_authors, articles + new_articles


def save(authors, articles):
    """
    Saves data into file in rewrite mode
    :param authors: list
    :param articles: list
    :return: void
    """
    with open(storage_name, 'w') as f:
        f.write(json.dumps({'authors': authors, 'articles': articles}, indent=2))


def read():
    """
    Reads data from file
    :return: authors, articles
    """
    if not os.path.isfile(storage_name):
        with open(storage_name, 'w') as f:
            pass

    with open(storage_name, 'r+') as f:
        content = f.read()
        if content:
            data = json.loads(content)
            return data['authors'], data['articles']
    return [], []

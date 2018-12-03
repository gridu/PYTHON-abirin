
import json
import os.path
from datetime import datetime
import logging

storage_name = 'articles.txt'
logger = logging.getLogger('report.storage')


def read_new(_authors, _articles):
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
    with open(storage_name, 'w') as f:
        f.write(json.dumps({'authors': authors, 'articles': articles}, indent=2))


def read():
    if not os.path.isfile(storage_name):
        with open(storage_name, 'w') as f:
            pass

    with open(storage_name, 'r+') as f:
        content = f.read()
        if content:
            data = json.loads(content)
            return data['authors'], data['articles']
    return [], []

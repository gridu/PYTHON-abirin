from storage import read, change_storage
from visualizer import get_top_authors_articles
import unittest

test_data = 'articles_test.txt'


class TestVisualize(unittest.TestCase):

    def test_top_data(self):
        change_storage(test_data)
        authors, articles = read()
        top_authors, top_articles = get_top_authors_articles(authors, articles)

        self.assertEqual(len(top_articles), 5)
        self.assertEqual(len(top_authors), 5)

        author_names = [author['name'] for author in top_authors]
        article_titles = [article['title'] for article in top_articles]
        self.assertEqual(author_names, ['author1', 'author2',
                                        'author3', 'author4', 'author5'])
        self.assertEqual(article_titles, ['article7', 'article6',
                                          'article5', 'article4', 'article3'])


if __name__ == '__main__':
    unittest.main()

from storage import read_new, save, change_storage
import unittest
import os

file_name = 'test_storage.txt'


class StorageTest(unittest.TestCase):

    def test_read_new_empty(self):
        self.prepare_storage()

        authors, articles = read_new([], [])
        self.assertFalse(authors)
        self.assertFalse(articles)

    def test_save_empty(self):
        self.prepare_storage()

        save([], [])
        self.assertTrue(os.path.exists(file_name))

    def test_read_save(self):
        self.prepare_storage()
        save([{'name': 'author'}], [{'title': 'article', 'date': 1541631600.0}])
        authors, articles = read_new([{'name': 'author2'}], [{'title': 'article2', 'date': 1542236400.0}])
        self.assertEqual(len(articles), 2)
        self.assertEqual(len(authors), 2)

    def prepare_storage(self):
        if os.path.exists(file_name):
            os.remove(file_name)
        change_storage(file_name)


if __name__ == '__main__':
    unittest.main()

import mock
import unittest

import requests
from bs4 import BeautifulSoup

import backup
import main
from config import BASE_DIR, TIMER, URL, BACKUP_DIR, DIRNAMES


class BackUpTestCase(unittest.TestCase):

    def setUp(self):
        backup.urllib = mock.Mock()
        backup.os = mock.Mock()

    def test_is_abs_url(self):
        # Test is_abs_url

        # is abs url
        url = 'http://www.cwi.nl:80/%7Eguido/Python.html'
        self.assertEqual(backup.is_abs_url(url), 'http')

        # is not a abs url
        url = '/%7Eguido/Python.html'
        self.assertEqual(backup.is_abs_url(url), '')

    def test_create_external_file(self):
        pass


class MainTestCase(unittest.TestCase):

    def setUp(self):
        main.os = mock.Mock()
        main.os.path = mock.Mock()
        main.time = mock.Mock()
        main.BeautifulSoup = mock.Mock()
        main.requests = mock.Mock()
        self.path = 'path'
        main.os.path.join.return_value = self.path
        main.time.strftime.return_value = 'time'

    def test_mkdir(self):

        # test the dit has exists
        with mock.patch('main.os.path.exists', return_value=True):
            self.assertEqual(main.mkdir(BACKUP_DIR), self.path)
            main.os.path.join.assert_called_with(BASE_DIR, BACKUP_DIR, 'time')
            self.assertFalse(main.os.makedirs.called)

        # test the dir has not exists
        with mock.patch('main.os.path.exists', return_value=False):
            self.assertEqual(main.mkdir(BACKUP_DIR), self.path)
            main.os.makedirs.assert_called_with(self.path)
            self.assertEqual(main.os.makedirs.call_count, len(DIRNAMES))

    @mock.patch('main.mkdir')
    @mock.patch('main.backup')
    def test_main_back_up(self, mock_backup, mock_mkdir):

        mock_mkdir.return_value = self.path
        r = mock.Mock()
        # r.text = 'html'
        soup = 'soup'
        main.requests.get.return_value = r
        main.BeautifulSoup.return_value = soup
        main.back_up('url', 'backup_dir')

        mock_mkdir.assert_called_with('backup_dir')
        main.requests.get.assert_called_with('url')
        main.BeautifulSoup.assert_called_with(r.text, 'html.parser')
        mock_backup.js_backup.assert_called_with(soup, self.path)
        mock_backup.css_backup.assert_called_with(soup, self.path)
        mock_backup.images_backup.assert_called_with(soup, self.path)


if __name__ == '__main__':
    unittest.main()

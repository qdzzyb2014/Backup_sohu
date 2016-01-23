import mock
import unittest

import requests
from bs4 import BeautifulSoup

import backup
import main
from config import BASE_DIR, TIMER, URL, BACKUP_DIR, DIRNAMES


class BackUpTestCase(unittest.TestCase):

    def test_is_abs_url(self):
        # Test is_abs_url

        # is abs url
        url = 'http://www.cwi.nl:80/%7Eguido/Python.html'
        self.assertEqual(backup.is_abs_url(url), 'http')

        # is not a abs url
        url = '/%7Eguido/Python.html'
        self.assertEqual(backup.is_abs_url(url), '')


class MainTestCase(unittest.TestCase):

    def setUp(self):
        main.os = mock.Mock()
        main.os.path = mock.Mock()
        main.time = mock.Mock()
        main.BeautifulSoup = mock.Mock()
        main.requests = mock.Mock()
        main.os.path.join.return_value = 'path'
        main.time.strftime.return_value = 'time'

    def test_mkdir_dir_exist(self):
        main.os.path.exists.return_value = True

        self.assertEqual(main.mkdir(BACKUP_DIR), 'path')
        main.os.path.join.assert_called_with(BASE_DIR, BACKUP_DIR, 'time')

        self.assertFalse(main.os.makedirs.called)

    def test_mkdir_dir_not_exist(self):
        main.os.path.exists.return_value = False

        self.assertEqual(main.mkdir(BACKUP_DIR), 'path')

        main.os.makedirs.assert_called_with('path')
        self.assertEqual(main.os.makedirs.call_count, len(DIRNAMES))

    @mock.patch('main.mkdir')
    @mock.patch('main.backup')
    def test_main_back_up(self, mock_backup, mock_mkdir):
        mock_mkdir.return_value = 'path'
        r = mock.create_autospec(requests.Response)
        s = mock.create_autospec(BeautifulSoup)
        main.requests.get.return_value = r
        main.BeautifulSoup.return_value = s
        mock_backup.js_back.return_value = None
        mock_backup.css_back.return_value = None
        mock_backup.images_back.return_value = None

        main.back_up('url', 'backup_dir')

        mock_mkdir.assert_called_with('backup_dir')
        main.requests.get.assert_called_with('url')
        main.BeautifulSoup.assert_called_with(r.test, 'html.parser')


if __name__ == '__main__':
    unittest.main()

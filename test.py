# -*- coding: utf-8 -*-
import mock
import unittest

from StringIO import StringIO


import backup
import main
from config import BASE_DIR, BACKUP_DIR, DIRNAMES


class BackUpTestCase(unittest.TestCase):

    def setUp(self):
        backup.urllib = mock.Mock()
        backup.os = mock.Mock()
        self.path = 'path'
        self.soup = mock.Mock()

    def test_is_abs_url(self):
        # Test is_abs_url

        # is abs url
        url = 'http://www.cwi.nl:80/%7Eguido/Python.html'
        self.assertEqual(backup.is_abs_url(url), 'http')

        # is not a abs url
        url = '/%7Eguido/Python.html'
        self.assertEqual(backup.is_abs_url(url), '')

    @mock.patch('backup.urllib')
    def test_create_external_file(self, mock_urllib):
        t_tag = mock.Mock()
        t_tag.get.return_value = 'target'
        get_arg = 'src'
        path = 'path'
        backup.os.path.join.return_value = 'filepath'
        with mock.patch('backup.os.path.exists', return_value=True):
            backup.create_external_file(t_tag, get_arg, path)
            t_tag.get.assert_called_with(get_arg)
            self.assertFalse(mock_urllib.urlretrieve.called)

        with mock.patch('backup.os.path.exists', return_value=False):
            backup.create_external_file(t_tag, get_arg, path)
            mock_urllib.urlretrieve.assert_called_with(
                'target', 'filepath')

    def test_create_inline_file(self):
        mock_open = mock.mock_open()
        t_tag = mock.Mock()
        t_tag.text = 'text'
        backup.os.path.join.return_value = 'final path'
        with mock.patch('backup.open', mock_open):
            backup.create_inline_file(t_tag, 'path', 'fe', 1)

            mock_open.assert_called_once_with('final path', 'wb')
            mock_open().write.assert_called_once_with('text')

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_html_backup(self, mock_stdout):
        mock_open = mock.mock_open()
        self.soup.prettify.return_value = 'entire html'
        backup.os.path.join.return_value = 'html path'
        with mock.patch('backup.open', mock_open):
            backup.html_backup(self.soup, self.path)

            mock_open.assert_called_once_with('html path', 'wb')
            mock_open().write.assert_called_once_with('entire html')
            self.assertTrue(mock_stdout.getvalue() == 'HTML has backed up.\n')

    @mock.patch('backup.create_external_file')
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_images_backup(self, mock_stdout, mock_create_external_file):
        self.soup.find_all.return_value = []
        backup.images_backup(self.soup, self.path)
        self.assertFalse(mock_create_external_file.called)
        self.assertTrue(mock_stdout.getvalue() == 'There is no images.\n')

        mock_create_external_file.reset_mock()
        self.soup.find_all.return_value = [1, 2, 3]

        backup.images_backup(self.soup, self.path)
        self.soup.find_all.assert_called_with('img')
        backup.os.path.join.assert_called_with(self.path, 'images')
        self.assertTrue(
            mock_create_external_file.call_count ==
            len(self.soup.find_all()))
        self.assertTrue(
            mock_stdout.getvalue().endswith('Iamges had backed up.\n'))

    @mock.patch('backup.create_inline_file')
    @mock.patch('backup.create_external_file')
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_css_backup(self, mock_stdout, mock_ex_file, mock_inline_file):
        self.soup.find_all.return_value = []
        backup.css_backup(self.soup, self.path)
        self.assertFalse(mock_ex_file.called)
        self.assertFalse(mock_inline_file.called)

        self.soup.find_all.return_value = [1, 2, 3]
        mock_ex_file.reset_mock()
        mock_inline_file.reset_mock()
        backup.css_backup(self.soup, self.path)
        self.assertTrue(
            mock_ex_file.call_count == mock_inline_file.call_count)
        self.assertTrue(
            mock_stdout.getvalue().endswith('CSS has backed up.\n'))

    @mock.patch('backup.create_inline_file')
    @mock.patch('backup.create_external_file')
    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('bs4.Tag')
    def test_js_backup(self, mock_tag, mock_stdout,
                       mock_ex_file, mock_inline_file):
        # init
        mock_tag.has_attr.return_value = True
        js_list = []

        # if no js
        self.soup.find_all.return_value = js_list
        backup.js_backup(self.soup, self.path)
        self.assertTrue(mock_stdout.getvalue() == 'There is no js.\n')
        self.assertFalse(mock_ex_file.called)
        self.assertFalse(mock_inline_file.called)

        # else
        for i in xrange(5):
            js_list.append(mock_tag())
        self.soup.find_all.return_value = js_list
        backup.os.path.join.return_value = 'js path'
        backup.js_backup(self.soup, self.path)

        mock_ex_file.assert_called_with(js_list[3], 'src', 'js path')
        self.assertTrue(mock_ex_file.call_count == 5)
        self.assertTrue(mock_inline_file.call_count == 0)
        self.assertTrue(mock_stdout.getvalue().endswith('js had backed up.\n'))


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

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_mkdir(self, mock_stdout):

        # test the dit has exists
        with mock.patch('main.os.path.exists', return_value=True):
            self.assertEqual(main.mkdir(BACKUP_DIR), self.path)
            main.os.path.join.assert_called_with(BASE_DIR, BACKUP_DIR, 'time')
            self.assertFalse(main.os.makedirs.called)
            self.assertTrue(mock_stdout.getvalue() == 'doc has existed\n')

        # test the dir has not exists
        with mock.patch('main.os.path.exists', return_value=False):
            self.assertEqual(main.mkdir(BACKUP_DIR), self.path)
            main.os.makedirs.assert_called_with(self.path)
            self.assertEqual(main.os.makedirs.call_count, len(DIRNAMES) - 1)

    @mock.patch('main.mkdir')
    @mock.patch('main.backup')
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_main_back_up(self, mock_stdout, mock_backup, mock_mkdir):

        mock_mkdir.return_value = self.path
        r = mock.Mock()
        # r.text = 'html'
        soup = 'soup'
        main.requests.get.return_value = r
        main.BeautifulSoup.return_value = soup
        main.back_up('url', 'backup_dir')

        self.assertTrue(mock_stdout.getvalue() == 'time\n')
        mock_mkdir.assert_called_with('backup_dir')
        main.requests.get.assert_called_with('url')
        main.BeautifulSoup.assert_called_with(r.text, 'html.parser')
        mock_backup.js_backup.assert_called_with(soup, self.path)
        mock_backup.css_backup.assert_called_with(soup, self.path)
        mock_backup.images_backup.assert_called_with(soup, self.path)


if __name__ == '__main__':
    unittest.main()

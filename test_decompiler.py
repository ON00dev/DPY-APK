import unittest
from unittest.mock import patch, MagicMock
import subprocess
import os
import dpy_apk
import logging

class TestDecompiler(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.apk_path = '/your/apk/file/path'
        self.extracted_dir = './extracted_apk'
        self.smali_output_dir = './smali_output'
        self.dex_path = os.path.join(self.extracted_dir, 'classes.dex')

    @patch('os.path.isfile')
    def test_verify_file_path(self, mock_isfile):
        mock_isfile.return_value = True
        try:
            dpy_apk.verify_file_path(self.apk_path)
        except FileNotFoundError:
            self.fail("verify_file_path() raised FileNotFoundError unexpectedly!")

        mock_isfile.return_value = False
        with self.assertRaises(FileNotFoundError):
            dpy_apk.verify_file_path(self.apk_path)

    @patch('os.makedirs')
    @patch('os.path.exists')
    def test_create_output_dir(self, mock_exists, mock_makedirs):
        mock_exists.return_value = False
        try:
            dpy_apk.create_output_dir(self.extracted_dir)
        except RuntimeError:
            self.fail("create_output_dir() raised RuntimeError unexpectedly!")

        mock_exists.return_value = True
        try:
            dpy_apk.create_output_dir(self.extracted_dir)
        except RuntimeError:
            self.fail("create_output_dir() raised RuntimeError unexpectedly!")

        mock_makedirs.side_effect = OSError("Error creating directory")
        with self.assertRaises(RuntimeError):
            dpy_apk.create_output_dir(self.extracted_dir)

    @patch('subprocess.run')
    @patch('dpy_apk.create_output_dir')
    def test_unzip_apk(self, mock_create_output_dir, mock_subprocess_run):
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        try:
            dpy_apk.unzip_apk(self.apk_path, self.extracted_dir)
        except RuntimeError:
            self.fail("unzip_apk() raised RuntimeError unexpectedly!")

        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'unzip')
        with self.assertRaises(RuntimeError):
            dpy_apk.unzip_apk(self.apk_path, self.extracted_dir)

    @patch('subprocess.run')
    def test_decompile_dex_to_smali(self, mock_subprocess_run):
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        try:
            dpy_apk.decompile_dex_to_smali(self.dex_path, self.smali_output_dir)
        except RuntimeError:
            self.fail("decompile_dex_to_smali() raised RuntimeError unexpectedly!")

        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'java')
        with self.assertRaises(RuntimeError):
            dpy_apk.decompile_dex_to_smali(self.dex_path, self.smali_output_dir)

if __name__ == '__main__':
    unittest.main()

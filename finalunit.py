import unittest
from tkinter import Tk
from tkinter import filedialog
from PIL import Image
from stegano import lsb
import os
from io import StringIO
import sys


from your_steganography_app import StegoApp

class TestStegoApp(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = StegoApp(self.root)
        self.filename = None

    def tearDown(self):
        self.root.destroy()

    def test_show_image(self):
        self.app.show_image()
        self.assertTrue(self.app.image_label.image is not None)

    def test_hide_and_show_data(self):
        message = "This is a test message."
        self.app.text_area.insert('1.0', message)

        with StringIO() as captured_output:
            sys.stdout = captured_output
            self.app.hide_data()
            sys.stdout = sys.__stdout__

        self.filename = self.app.filename
        self.assertTrue(os.path.exists(self.filename))

        clear_message = lsb.reveal(self.filename)
        self.assertEqual(clear_message.strip(), message.strip())

    def test_save_image(self):
        self.app.filename = "test_image.png"
        self.app.secret = lsb.hide("sample.png", "Test message.")
        self.app.save_image()
        self.assertTrue(os.path.exists("hidden.png"))

if __name__ == '__main__':
    unittest.main()

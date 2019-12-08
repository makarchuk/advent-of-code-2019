import unittest
from main import Image

class Tests(unittest.TestCase):
    def test_layers_parse(self):
        data = "123456789012"
        img = Image(2, 3, data)
        self.assertEqual(img.layers, [
            [1, 2, 3, 4, 5, 6],
            [7, 8, 9, 0, 1, 2]
        ])
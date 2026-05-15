import unittest


class MyTest(unittest.TestCase):
    def testColors(self):
        self.assertEqual(
            self.string_output(), r'\override Stem.color = "darkgreen"' "\n"
        )

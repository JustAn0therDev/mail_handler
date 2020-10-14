import unittest
from config import Config


class MyTestCase(unittest.TestCase):
    def test_config(self):
        config = Config()
        self.assertTrue(config.email is not None)
        self.assertTrue(config.password is not None)


if __name__ == '__main__':
    unittest.main()

import unittest
from config import Config
from imap_connection_handler import ImapConnectionHandler


class MyTestCase(unittest.TestCase):
    def test_that_no_obligatory_config_prop_is_empty(self):
        config = Config('configs.txt')
        self.assertTrue(config.email is not None)
        self.assertTrue(config.app_password is not None)
        self.assertTrue(config.search is not None)
        self.assertTrue(config.data_to_look_for is not None)
        self.assertTrue(config.mailbox is not None)
        self.assertTrue(config.imap_address is not None)

    def test_imap_connection_handler_instance(self):
        config = Config('configs.txt')
        imap_connection_handler = ImapConnectionHandler(config)
        self.assertTrue(imap_connection_handler is not None)


if __name__ == '__main__':
    unittest.main()

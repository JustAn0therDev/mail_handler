import os
import unittest
from pathlib import Path
from config import Config
from io_handler import IOHandler
from imap_connection_handler import ImapConnectionHandler


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.__config = Config('testing_configs.txt')
        self.__imap_connection_handler = ImapConnectionHandler(self.__config)

    def test_that_no_obligatory_config_prop_is_empty(self):
        self.assertTrue(self.__config.email is not None)
        self.assertTrue(self.__config.app_password is not None)
        self.assertTrue(self.__config.search is not None)
        self.assertTrue(self.__config.data_to_look_for is not None)
        self.assertTrue(self.__config.mailbox is not None)
        self.assertTrue(self.__config.imap_address is not None)
        self.assertTrue(self.__config.action is not None)

    def test_imap_connection_handler_instance_is_not_none(self):
        self.assertTrue(self.__imap_connection_handler is not None)

    def test_selection_result_validation_should_throw_exception(self):
        with self.assertRaises(expected_exception=Exception) as assertRaises:
            ImapConnectionHandler.validate_selection_result('NOK')
        raised_exception = assertRaises.exception
        self.assertEqual(str(raised_exception), 'The specified mailbox could not be found or accessed')

    def test_execute_instructions_from_config_values(self):
        file_name = '{}/message_output_0.txt'.format(self.__config.save_file_path)
        self.__imap_connection_handler.execute_instructions_from_config_values()
        self.assertTrue(Path(file_name).stat().st_size > 0)
        os.remove(file_name)

    def test_attachment_download(self):
        self.__imap_connection_handler.execute_instructions_from_config_values()

    def test_io_handling_sys_args_validation(self):
        with self.assertRaises(expected_exception=SystemExit) as assertRaises:
            IOHandler.validate_arguments(['nothing'])
        raised_exception = assertRaises.exception
        self.assertEqual(raised_exception.code, 1)


if __name__ == '__main__':
    unittest.main()


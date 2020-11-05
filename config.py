from typing import Dict
from io_handler import IOHandler


class Config:
    __dictionary_of_configs: Dict
    save_file_name: str
    extension: str
    to_addresses: str

    def initialize_default_config_values(self):
        self.save_file_name = 'message_output'
        self.extension = 'txt'

    def __init__(self, file_path: str):
        self.__dictionary_of_configs = IOHandler.get_dictionary_of_configs_from_file(file_path)
        self.email = self.__dictionary_of_configs['EMAIL']
        self.app_password = self.__dictionary_of_configs['APP_PASSWORD']
        self.search = self.__dictionary_of_configs['SEARCH']
        self.data_to_look_for = self.__dictionary_of_configs['DATA_TO_LOOK_FOR']
        self.mailbox = self.__dictionary_of_configs['MAILBOX']
        self.imap_address = self.__dictionary_of_configs['IMAP_ADDRESS']
        self.smtp_address = self.__dictionary_of_configs['SMTP_ADDRESS']
        self.save_file_path = self.__dictionary_of_configs['OUTPUT']
        self.action = self.__dictionary_of_configs['ACTION']
        self.to_addresses = self.__dictionary_of_configs['TO']
        self.initialize_default_config_values()


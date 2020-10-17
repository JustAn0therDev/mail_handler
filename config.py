from io_handler import IOHandler


class Config:

    def __init__(self, file_path: str):
        dictionary_of_configs = IOHandler.get_dictionary_of_configs_from_file(file_path)

        self.email = dictionary_of_configs['EMAIL']
        self.app_password = dictionary_of_configs['APP_PASSWORD']
        self.search = dictionary_of_configs['SEARCH']
        self.data_to_look_for = dictionary_of_configs['DATA_TO_LOOK_FOR']
        self.mailbox = dictionary_of_configs['MAILBOX']
        self.imap_address = dictionary_of_configs['IMAP_ADDRESS']
        self.save_file_path = dictionary_of_configs['OUTPUT']
        self.save_file_name = 'message_output'

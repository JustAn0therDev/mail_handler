from config import Config
import sys
from imap_connection_handler import ImapConnectionHandler
from io_handler import IOHandler

try:
    IOHandler.validate_arguments(sys.argv)
    config = Config(file_path=sys.argv[1])
    imap_connection_handler = ImapConnectionHandler(config)
    imap_connection_handler.execute_instructions_from_config_values()
except Exception as error:
    print(f'[EXCEPTION] - An unexpected error occurred: {str(error)}')

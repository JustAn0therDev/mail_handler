#!/usr/bin/env python3

import sys
from config import Config
from io_handler import IOHandler
from imap_connection_handler import ImapConnectionHandler


try:
    IOHandler.validate_arguments(sys.argv)
    config = Config(file_path=sys.argv[1])
    imap_connection_handler = ImapConnectionHandler(config)
    imap_connection_handler.execute_instructions_from_config_values()
except Exception as error:
    print('[EXCEPTION] {}'.format(str(error)))

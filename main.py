from config import Config
from imap_connection_handler import ImapConnectionHandler

try:
    # file_path = sys.argv[1]
    imap_connection_handler = ImapConnectionHandler(Config('configs.txt'))
    imap_connection_handler.execute_while_in_imap_connection()
except Exception as error:
    print('An error occurred: {}'.format(str(error)))

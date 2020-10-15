from imaplib import IMAP4_SSL, IMAP4
import email
from config import Config

"""
    IMPROVE: have a "send_message" in this class to
    send it to an specific socked/RESTful API route    
"""


class ImapConnectionHandler:
    def __init__(self, config: Config):
        self.__config = config

    def execute_while_in_imap_connection(self) -> None:
        with IMAP4_SSL(self.__config.imap_address) as imap_connection:
            self.__login(imap_connection)
            self.__select_mailbox(imap_connection)
            _, email_data = self.__search_mailbox(imap_connection)
            self.__write_message_body_to_file(imap_connection, email_data)
            imap_connection.close()

    def __login(self, imap_connection: IMAP4) -> None:
        imap_connection.login(self.__config.email, self.__config.app_password)

    def __select_mailbox(self, imap_connection: IMAP4) -> None:
        imap_connection.select(self.__config.mailbox)

    def __search_mailbox(self, imap_connection: IMAP4) -> tuple:
        return imap_connection.search(None, self.__config.search, self.__config.data_to_look_for)

    def __write_message_body_to_file(self, imap_connection: IMAP4,  email_data: list) -> None:
        with open('test.txt', 'w') as file:
                for value in email_data[0].split():
                    # data has a type of tuple(bytes, bytes)
                    _, data = imap_connection.fetch(value, '(RFC 822)')
                    if data[0] is not None:
                        raw_email_data: bytearray = data[0][1]
                        raw_email_string: str = raw_email_data.decode('utf-8')
                        email_message: email = email.message_from_string(raw_email_string)
                        text_plain_message: str = ''
                        if email_message.is_multipart():
                            for payload in email_message.walk():
                                content_type = payload.get_content_type()
                                content_disposition = str(payload.get('Content-Disposition'))
                                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                                    try:
                                        text_plain_message = payload.get_payload(decode=True).decode('latin-1')
                                        file.write('{}\n'.format(text_plain_message))
                                    except Exception as error:
                                        print(f'parsing error: {error}')
                                        pass
                        else:
                            content_type = email_message.get_content_type()
                            content_disposition = str(email_message.get('Content-Disposition'))
                            if content_type == 'text/plain' and 'attachment' not in content_disposition:
                                text_plain_message = email_message.get_payload(decode=True).decode('latin-1')
                                file.write('{}\n'.format(text_plain_message))

    def __download_message_attachment(self) -> None:
        pass

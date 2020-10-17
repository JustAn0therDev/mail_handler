from imaplib import IMAP4_SSL, IMAP4
import email
from typing import Union

from config import Config
from io_handler import IOHandler


class ImapConnectionHandler:
    def __init__(self, config: Config):
        self.__config = config

    def execute_instructions_from_config_values(self) -> None:
        with IMAP4_SSL(self.__config.imap_address) as imap_connection:
            self.__login(imap_connection)
            self.__select_mailbox(imap_connection)
            _, email_data = self.__search_mailbox(imap_connection)

            """
                TODO: condition here to check if the config file tells the
                code to write message body to a file or download an e-mail attachment
            """

            self.__try_write_message_body_to_file(imap_connection, email_data)
            imap_connection.close()

    def __login(self, imap_connection: IMAP4) -> None:
        imap_connection.login(self.__config.email, self.__config.app_password)

    def __select_mailbox(self, imap_connection: IMAP4) -> None:
        imap_connection.select(self.__config.mailbox)

    def __search_mailbox(self, imap_connection: IMAP4) -> tuple:
        return imap_connection.search(None, self.__config.search, self.__config.data_to_look_for)

    def __try_write_message_body_to_file(self, imap_connection: IMAP4, email_data: list) -> None:
        if len(email_data) > 0:
            IOHandler.truncate_file_content(self.__config.save_file_path)
            for value in email_data[0].split():
                _, data = imap_connection.fetch(value, '(RFC822)')
                if data[0] is not None:
                    email_message = ImapConnectionHandler.__get_email_message(data)
                    if email_message.is_multipart():
                        for payload in email_message.walk():
                            IOHandler.write_payload_to_file(
                                payload=payload.get_payload(decode=True),
                                content_type=payload.get_content_type(),
                                content_disposition=str(payload.get('Content-Disposition')),
                                file_path=self.__config.save_file_path)
                    else:
                        IOHandler.write_payload_to_file(
                            payload=email_message.get_payload(decode=True),
                            content_type=email_message.get_content_type(),
                            content_disposition=str(email_message.get('Content-Disposition')),
                            file_path=self.__config.save_file_path)
                else:
                    print("No message was found for the specified criteria in the configuration file")

    @staticmethod
    def __get_email_message(data: Union[list, list]) -> email:
        raw_email_data: bytearray = data[0][1]
        return email.message_from_string(s=raw_email_data.decode('utf-8'))

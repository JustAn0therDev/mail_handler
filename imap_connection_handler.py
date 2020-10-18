from imaplib import IMAP4_SSL, IMAP4
import email
import os
from typing import Tuple, List, Union
from config import Config
from smtp_connection_handler import SmtpConnectionHandler
from io_handler import IOHandler


class ImapConnectionHandler:
    def __init__(self, config: Config, ):
        self.__smtp_connection_handler = SmtpConnectionHandler(config)
        self.__config = config

    def execute_instructions_from_config_values(self) -> None:
        with IMAP4_SSL(self.__config.imap_address) as imap_connection:
            self.__login(imap_connection)
            self.__select_mailbox(imap_connection)
            _, email_data = self.__search_mailbox(imap_connection)

            if self.__config.action.lower() == 'text':
                self.__try_write_message_body_to_file(imap_connection, email_data)
            elif self.__config.action.lower() == 'attachment':
                self.__try_download_attachments_to_path(imap_connection, email_data)
            elif self.__config.action.lower() == 'forward':
                self.__send_email_data_with_smtp(imap_connection, email_data)
            else:
                raise NotImplementedError('The specified ACTION value in the config file has not been implemented yet')

    def __login(self, imap_connection: IMAP4) -> None:
        imap_connection.login(self.__config.email, self.__config.app_password)

    def __select_mailbox(self, imap_connection: IMAP4) -> None:
        selection_result, _ = imap_connection.select(self.__config.mailbox)
        ImapConnectionHandler.validate_selection_result(selection_result)

    @staticmethod
    def validate_selection_result(selection_result: str):
        if selection_result != 'OK':
            raise Exception('The specified mailbox could not be found or accessed')

    def __search_mailbox(self, imap_connection: IMAP4) -> Tuple[str, list]:
        return imap_connection.search(None, self.__config.search, self.__config.data_to_look_for)

    def __try_write_message_body_to_file(self, imap_connection: IMAP4, email_data: List[Tuple[bytes, bytes]]) -> None:
        if len(email_data) > 0:
            for i, mail in enumerate(email_data[0].split()):
                file_path = \
                    f'{self.__config.save_file_path}/{self.__config.save_file_name}_{i + 1}.{self.__config.extension}'
                _, email_bytes_tuple = imap_connection.fetch(mail, '(RFC822)')
                if email_bytes_tuple[0] is not None:
                    IOHandler.truncate_file_content(file_path)
                    email_message = ImapConnectionHandler.__get_email_message_from_bytes_tuple(email_bytes_tuple)
                    if email_message.is_multipart():
                        for part in email_message.walk():
                            IOHandler.write_payload_to_file(
                                payload=part.get_payload(decode=True),
                                content_type=part.get_content_type(),
                                content_disposition=str(part.get('Content-Disposition')),
                                file_path=file_path)
                    else:
                        IOHandler.write_payload_to_file(
                            payload=email_message.get_payload(decode=True),
                            content_type=email_message.get_content_type(),
                            content_disposition=str(email_message.get('Content-Disposition')),
                            file_path=file_path)
                else:
                    print('No information was found for the searched message')

    def __try_download_attachments_to_path(self, imap_connection: IMAP4, email_data: List[Tuple[bytes, bytes]]) -> None:
        for i, mail in enumerate(email_data[0].split()):
            _, email_bytes_tuple = imap_connection.fetch(mail, '(RFC822)')
            email_message = ImapConnectionHandler.__get_email_message_from_bytes_tuple(email_bytes_tuple)
            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                    continue
                if os.path.exists(f'{self.__config.save_file_path}/{part.get_filename()}'):
                    attachment_name, extension = part.get_filename().split(".")[0], part.get_filename().split(".")[1]
                    file_name = f'{attachment_name}_{i}.{extension}'
                    file_path = f'{self.__config.save_file_path}/{file_name}'
                    with open(file_path, 'wb') as byte_writer:
                        byte_writer.write(part.get_payload(decode=True))
                else:
                    file_path = f'{self.__config.save_file_path}/{part.get_filename()}'
                    with open(file_path, 'wb') as byte_writer:
                        byte_writer.write(part.get_payload(decode=True))

    @staticmethod
    def __get_email_message_from_bytes_tuple(email_data_in_bytes: Union[List[None], List[Union[bytes, Tuple[bytes, bytes]]]]) -> email:
        return email.message_from_string(s=email_data_in_bytes[0][1].decode('utf-8'))

    def __send_email_data_with_smtp(self, imap_connection: IMAP4, email_data: List[Tuple[bytes, bytes]]):
        list_of_email_messages = []
        for i, mail in enumerate(email_data[0].split()):
            _, email_bytes_tuple = imap_connection.fetch(mail, '(RFC822)')
            list_of_email_messages.append(ImapConnectionHandler.__get_email_message_from_bytes_tuple(email_bytes_tuple))
        self.__smtp_connection_handler.send_email_data_to_config_addresses(list_of_email_messages)

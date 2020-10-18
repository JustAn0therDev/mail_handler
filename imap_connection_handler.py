from imaplib import IMAP4_SSL, IMAP4
import email
from pathlib import Path
from typing import Tuple, List
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

            if self.__config.what_to_download.lower() == 'text_content':
                self.__try_write_message_body_to_file(imap_connection, email_data)
            elif self.__config.what_to_download.lower() == 'attachment':
                self.__try_download_attachments_to_path(imap_connection, email_data)
            else:
                raise NotImplemented('The specified DOWNLOAD value in the config file has not been implemented yet')

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

    def __try_write_message_body_to_file(self, imap_connection: IMAP4, email_data: list) -> None:
        if len(email_data) > 0:
            for i, mail in enumerate(email_data[0].split()):
                file_path = f'{self.__config.save_file_path}/{self.__config.save_file_name}_{i}.txt'
                _, email_data_in_bytes = imap_connection.fetch(mail, '(RFC822)')
                if email_data_in_bytes[0] is not None:
                    IOHandler.truncate_file_content(file_path)
                    email_message = ImapConnectionHandler.__get_email_message(email_data_in_bytes)
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
                    print('No message was found for the specified criteria in the configuration file')

    def __try_download_attachments_to_path(self, imap_connection: IMAP4, email_data: list) -> None:
        for i, mail in enumerate(email_data[0].split()):
            _, email_data = imap_connection.fetch(mail, '(RFC822)')
            raw_email = email_data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                    continue
                if Path(f'{self.__config.save_file_path}/{part.get_filename()}').exists():
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
    def __get_email_message(email_data_in_bytes: List[Tuple[bytes, bytes]]) -> email:
        return email.message_from_string(s=email_data_in_bytes[0][1].decode('utf-8'))

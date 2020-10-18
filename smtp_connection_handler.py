from config import Config
from smtplib import SMTP_SSL


class SmtpConnectionHandler:
    def __init__(self, config: Config):
        self.__config = config

    def send_email_data_to_config_addresses(self, list_of_email_messages: list):
        with SMTP_SSL(self.__config.smtp_address) as smtp_connection:
            smtp_connection.login(self.__config.email, self.__config.app_password)
            for mail in list_of_email_messages:
                mail.replace_header('From', self.__config.email)
                mail.replace_header('To', self.__config.to_addresses)
                smtp_connection.sendmail(
                    self.__config.email,
                    self.__config.to_addresses.split(', '),
                    mail.as_string())

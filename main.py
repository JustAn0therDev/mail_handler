from imaplib import IMAP4_SSL
import email
import os
from config import Config

config = Config(search='FROM', data_to_search_for='test@gmail.com')

try:
    with IMAP4_SSL(host='imap.gmail.com') as email_inbox_connection:
        email_inbox_connection.login(config.email, config.password)
        email_inbox_connection.select('inbox')

        """ 
        don't know if 'type' value returned from search method will have it's use,
        so I'll be discarding it for now 
        """
        _, data = email_inbox_connection.search(None, config.search, config.data_to_search_for)

        for value in data[0].split():
            _, data = email_inbox_connection.fetch(value, '(RFC822)')
            raw_email_data: bytearray = data[0][1]
            raw_email_string = raw_email_data.decode('utf-8')
            email_body = email.message_from_string(raw_email_string)
            if email_body.is_multipart():
                for payload in email_body.walk():
                    content_type = payload.get_content_type()
                    content_disposition = str(payload.get('Content-Disposition'))
                    if content_type == 'text/plain' and 'attachment' not in content_disposition:
                        print(f'{payload.get_payload(decode=True).decode("utf-8")}')
            else:
                print(f'{email_body.get_payload(decode=True)}')

        email_inbox_connection.close()
except Exception as error:
    print('An error occurred: {}'.format(str(error)))

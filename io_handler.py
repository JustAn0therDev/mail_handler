import email


class IOHandler:
    @staticmethod
    def validate_arguments(argv: list) -> None:
        if len(argv) != 2:
            print('No configuration file path provided')
            quit(1)

    @staticmethod
    def get_dictionary_of_configs_from_file(file_path: str) -> dict:
        dict_of_configs = dict()
        with open(file_path, 'r', encoding='utf-8') as file_reader:
            for line in file_reader:
                current_line = line.split('=')
                dict_of_configs[current_line[0]] = current_line[1].replace('\n', '')
        return dict_of_configs

    @staticmethod
    def truncate_file_content(file_path: str) -> None:
        with open(file_path, 'w') as file_writer:
            initial_file_position = 0
            file_writer.seek(initial_file_position)
            file_writer.truncate()

    @staticmethod
    def write_payload_to_file(payload: email, content_type: str, content_disposition: str, file_path: str) -> None:
        try:
            with open(file_path, 'a') as file_writer:
                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    text_plain_message = payload.decode('utf-8')
                    file_writer.write('{}\n'.format(text_plain_message))
        except Exception as ex_error:
            print('[EXCEPTION] - File Writing: {}'.format(str(ex_error)))

    @staticmethod
    def save_email_attachment(email_content: email, content_disposition: str, file_path: str) -> None:
        try:
            with open(f'{file_path}', 'wb') as byte_writer:
                if 'attachment' in content_disposition:
                    byte_writer.write(email_content.get_payload(decode=True))
        except Exception as ex_error:
            print('[EXCEPTION] - While saving attachment: {}'.format(str(ex_error)))

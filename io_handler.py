import email


class IOHandler:
    @staticmethod
    def validate_arguments(argv: list) -> None:
        if len(argv) != 2:
            print('No configuration file provided')
            quit(1)

    @staticmethod
    def get_dictionary_of_configs_from_file(file_path: str) -> dict:
        dict_of_configs = dict()
        with open(file_path, 'r') as file_reader:
            for line in file_reader:
                current_line = line.split('=')
                dict_of_configs[current_line[0]] = current_line[1].replace('\n', '')
        return dict_of_configs

    @staticmethod
    def truncate_file_content(file_path: str) -> None:
        with open(file_path, 'w') as file_writer:
            initial_file_position_in_bytes = 0
            file_writer.seek(initial_file_position_in_bytes)
            file_writer.truncate()

    @staticmethod
    def write_payload_to_file(payload: email, content_type: str, content_disposition: list, file_path: str) -> None:
        try:
            with open(file_path, 'a') as file_writer:
                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    text_plain_message = payload.decode('utf-8')
                    file_writer.write('{}\n'.format(text_plain_message))
        except Exception as ex_error:
            print(f'[EXCEPTION] - File Writing: {ex_error}')

    @staticmethod
    def download_email_attachment(self) -> None:
        pass


import re
import validators


class InputValidator:
    @staticmethod
    def valid_string(user_input):
        if isinstance(user_input.strip(), str):
            return user_input
        return False

    @staticmethod
    def valid_number(user_input):
        if isinstance(user_input, (int, float)):
            if user_input >= 1:
                return user_input
        return False

    @staticmethod
    def valid_email(user_input):
        is_valid = re.search(r'^\w+@\w+.\w+$', user_input)
        if is_valid:
            return user_input
        return False

    @staticmethod
    def valid_image(user_input):
        if validators.url(user_input):
            return user_input
        return False

import os
import re

from dotenv import load_dotenv, find_dotenv

from utils.lexicon.load_lexicon import load_lexicon


class Validator:
    def __init__(self):
        load_dotenv(find_dotenv())

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

    async def validate_title(self, title: str) -> (bool, str):
        max_title_chars_length = int(os.environ["MAX_TITLE_CHARS_LENGTH"])

        if len(title) > max_title_chars_length:
            return False, self.replicas['general']['max_chars_length'] + f" {max_title_chars_length}"
        else:
            return True, ""

    async def validate_description(self, description: str) -> (bool, str):
        max_desc_chars_length = int(os.environ["MAX_DESC_CHARS_LENGTH"])

        if len(description) > max_desc_chars_length:
            return False, self.replicas['general']['max_chars_length'] + f" {max_desc_chars_length}"
        else:
            return True, ""

    async def validate_date(self, date: str) -> (bool, str):
        date_pattern = r"^(19|20)\d\d-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"

        if not re.match(date_pattern, date):
            return False, self.replicas['general']['date_pattern']
        else:
            return True, ""

    async def validate_link(self, link: str) -> (bool, str):
        max_link_chars_length = int(os.environ["MAX_LINK_CHARS_LENGTH"])

        if len(link) > max_link_chars_length:
            return False, self.replicas['general']['max_chars_length'] + f" {max_link_chars_length}"
        else:
            return True, ""

    async def validate_phone(self, phone: str) -> (bool, str):
        phone_pattern = r'^\+7 \(\d{3}\) \d{3} \d{2}-\d{2}$'

        if not re.match(phone_pattern, phone):
            return False, self.replicas['general']['phone_pattern']
        else:
            return True, ""

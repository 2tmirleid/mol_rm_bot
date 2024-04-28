import re


class EmailValidator:
    def __init__(self):
        self.regex = r"[^@]+@[^@]+\.[^@]+"

    def match(self, email):
        if re.match(self.regex, email) is not None:
            return True
        else:
            return False


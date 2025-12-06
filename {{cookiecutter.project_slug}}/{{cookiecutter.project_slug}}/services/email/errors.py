class EmailError(Exception):
    def __init__(self, message: str):
        self.message = message


class SendEmailError(EmailError):
    pass

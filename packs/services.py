from threading import Thread


class EmailSendThread(Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        Thread.__init__(self)

    def run(self):
        self.email_message.send()

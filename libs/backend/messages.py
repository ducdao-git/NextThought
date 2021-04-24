api_url = 'http://nsommer.wooster.edu/social'


class Message:
    """
    class repr a message between 2 user
    """

    def __init__(self, sender, senderid, recipient, recipientid,
                 content, time):
        """
        create a new message
        :param sender: string repr username of the sender
        :param senderid: int repr ID of the sender
        :param recipient: string repr username of the recipient
        :param recipientid: int repr ID of the recipient
        :param content: string repr content of the message
        :param time: string repr sent time of the message
        """
        self.sender = sender
        self.senderid = senderid
        self.recipient = recipient
        self.recipientid = recipientid
        self.content = content
        self.time = time

    def get_sender(self):
        """
        :return: string repr username of the sender
        """
        return self.sender

    def get_senderid(self):
        """
        :return: int repr ID of the sender
        """
        return self.senderid

    def get_recipient(self):
        """
        :return: string repr username of the recipient
        """
        return self.recipient

    def get_recipientid(self):
        """
        :return: int repr ID of the recipient
        """
        return self.recipientid

    def get_content(self):
        """
        :return: string repr content of the message
        """
        return self.content

    def get_time(self):
        """
        :return: string repr sent time of the message
        """
        return self.time

    def __repr__(self):
        """
        printable form of Message obj
        :return: string repr of a Message obj
        """
        return f'Message class -- sender: {self.senderid}, ' \
               f'recipient: {self.recipientid}, content: {self.content}'

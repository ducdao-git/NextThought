api_url = 'http://nsommer.wooster.edu/social'


class Message:
    def __init__(self, sender, senderid, recipient, recipientid,
                 content, time):
        self.sender = sender
        self.senderid = senderid
        self.recipient = recipient
        self.recipientid = recipientid
        self.content = content
        self.time = time

    def get_sender(self):
        """getter method to get sender"""
        return self.sender

    def get_senderid(self):
        """getter method to get senderid"""
        return self.senderid

    def get_recipient(self):
        """getter method to get recipient"""
        return self.recipient

    def get_recipientid(self):
        """getter method to get recipientid"""
        return self.recipientid

    def get_content(self):
        """getter method to get content"""
        return self.content

    def get_time(self):
        """getter method to get time"""
        return self.time

    def __repr__(self):
        return f'Message class -- sender: {self.sender}, ' \
               f'recipient: {self.recipient}, content: {self.content}'

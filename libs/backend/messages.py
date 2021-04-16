from pprint import pprint

from libs.backend.user import *

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


# user2 = AuthorizedUser('dtuser2', 'ejzifjyt')
# user3 = AuthorizedUser('dtuser3', 'sphyuddr')
#
# # user2.create_message(user3.get_uid(), 'msg 1 from user2 to user3')
# # user3.create_message(user2.get_uid(), 'msg 2 from user3 to user2')
#
# pprint(user2.get_conversations())
# pprint(user2.get_messages(user3.get_uid(), limit=1))
#
# print('\n')
# pprint(user3.get_conversations())
# pprint(user3.get_messages(user2.get_uid(), limit=1))

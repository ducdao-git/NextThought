from pprint import pprint

from libs.backend.user import *

api_url = 'http://nsommer.wooster.edu/social'

user2 = AuthorizedUser('dtuser2', 'ejzifjyt')
user3 = AuthorizedUser('dtuser3', 'sphyuddr')

# user2.create_message(user3.get_uid(), 'msg 1 from user2 to user3')
# user3.create_message(user2.get_uid(), 'msg 2 from user3 to user2')

pprint(user2.get_conversations())
pprint(user2.get_messages(user3.get_uid(), limit=1))

print('\n')
pprint(user3.get_conversations())
pprint(user3.get_messages(user2.get_uid(), limit=1))

import os
import time
import logging

from wannabe import wannabe
from maillist import maillist

logging.basicConfig(format='%(asctime)s %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.debug("started...")

# Connect to Wannabe
wannabe = wannabe(
    event_id=os.environ.get('EVENT_ID'),
    api_url=os.environ.get('API_URL'),
    client_id=os.environ.get('CLIENT_ID'),
    client_secret=os.environ.get('CLIENT_SECRET')
)

# Connect to Mailman
maillist = maillist(
    rest_url=os.environ.get('MAILMAN_REST_URL'),
    rest_username=os.environ.get('MAILMAN_REST_USERNAME'),
    rest_password=os.environ.get('MAILMAN_REST_PASSWORD'),
    domain=os.environ.get('DOMAIN')
)

running = True
while running:
    wb_maillist = wannabe.get_lists(os.environ.get('DOMAIN'))
    mailman_mailists = maillist.get_lists()

    todo_create = set(wb_maillist.keys()) - set(mailman_mailists)
    if len(todo_create) > 0:
        logger.info("Creating lists")
        for list in todo_create:
            logger.info(str(list))
            maillist.create_list(list=list)

    for list in wb_maillist.values():
        wb_members = wannabe.get_members_of_list(list)
        if maillist.sync_members(list['identifier'], wb_members) is True:
            logger.info(
                "List {} synced successfully".format(list['identifier'])
            )
        else:
            logger.error("Failed to sync members")

    time.sleep(600)

import os
import time
import logging
import signal
from http.client import HTTPConnection

from wannabe import wannabe
from maillist import maillist

HTTPConnection.debuglevel = 1

logging.basicConfig(format='%(asctime)s %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.INFO)
requests_log.propagate = True

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

def handle_timeout(signum, frame):
     logger.error("Run is taking to long, exit")
     raise Exception("end of time")

signal.signal(signal.SIGALRM, handle_timeout)

running = True
while running:
    # Start timer
    signal.alarm(60)
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

        logger.info("Sync finished: ".format(signal.alarm()))

    # Stop timer
    signal.alarm(0)
    time.sleep(600)

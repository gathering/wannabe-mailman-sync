import os
import time
import configparser
import logging
from pathlib import Path

from wannabe import wannabe
from maillist import maillist

logging.basicConfig(format='%(asctime)s %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

config = configparser.RawConfigParser()
config.read('config.ini')

logger.debug("started...")

# Connect to Wannabe
wannabe = wannabe(
    db_host='mysql',
    db_user=config['wannabe']['db_user'],
    db_password=config['wannabe']['db_password'],
    db_name=config['wannabe']['db_name'],
    event=config['wannabe']['event']
)

# Connect to MailMan
maillist = maillist(
    rest_url=config['mailman']['rest_url'],
    rest_username=config['mailman']['rest_username'],
    rest_password=config['mailman']['rest_password'],
    domain=config['mailman']['domain']
)

running = True

while running:
    wb_maillist = wannabe.get_lists(config['mailman']['domain'])
    mailman_mailists = maillist.get_lists()

    todo_create = set(wb_maillist) - set(mailman_mailists)
    if len(todo_create) > 0:
        logger.info("Creating lists")
        for list in todo_create:
            logger.info(str(list))
            maillist.create_list(list=list)

    for list in wb_maillist:
        wb_members = wannabe.get_members_of_list(list)
        if maillist.sync_members(list, wb_members) is True:
            logger.info("List {} synced successfully".format(list))
        else:
            logger.error("Failed to sync members")

    Path('last_updated.txt').touch()
    time.sleep(600)

import os
import configparser
import json

from wannabe import wannabe
from maillist import maillist

config = configparser.RawConfigParser()
config.read('config.ini')

# Connect to wannabe
wannabe = wannabe(
    db_host='mysql',
    db_user=config['wannabe']['db_user'],
    db_password=config['wannabe']['db_password'],
    db_name=config['wannabe']['db_name'],
    event=config['wannabe']['event']
)

# Connect to Google Apps
maillist = maillist(
    rest_url=config['mailman']['rest_url'],
    rest_username=config['mailman']['rest_username'],
    rest_password=config['mailman']['rest_password'],
    domain=config['mailman']['domain']
)

wb_maillist = wannabe.get_lists(config['mailman']['domain'])
mailman_mailists = maillist.get_lists()

todo_create = set(wb_maillist) - set(mailman_mailists)
if len(todo_create) > 0:
    print("Creating lists")
    for list in todo_create:
        print(list)
        maillist.create_list(list=list)

for list in wb_maillist:
    wb_members = wannabe.get_members_of_list(list)
    print(maillist.sync_members(list, wb_members))

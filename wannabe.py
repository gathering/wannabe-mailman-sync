import pymysql

import re

class wannabe(object):
    """Wannabe SQL Client"""

    def __init__(self, **args):
        self.event = args['event']
        self.eventId = None
        self.connection = pymysql.connect(
            host=args['db_host'],
            user=args['db_user'],
            password=args['db_password'],
            db=args['db_name'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT id FROM wb4_events WHERE reference = %s", self.event)
        for data in self.cursor.fetchall():
            self.eventId = int(data['id'])
        if self.eventId is None:
            raise Exception('Event {} not found'.format(self.event))

    def get_lists(self, domain):
        wb_maillist = []

        self.cursor.execute("SELECT address FROM wb4_mailinglists WHERE event_id = %s", self.eventId)
        for data in self.cursor.fetchall():
            if data['address'].split('@')[1] == domain:
                wb_maillist.append(data['address'].lower())
        return wb_maillist

    def get_members_of_list(self, list):
        self.cursor.execute("SELECT id FROM wb4_mailinglists WHERE event_id = %s AND address = %s", (self.eventId, list))
        for data in self.cursor.fetchall():
            listId = data['id']
        members = []
        self.cursor.execute("call mailinglistaddresses(%s)", listId)
        for data in self.cursor.fetchall():
            user_email = re.sub(r'(\+.*?)(?=\@)', '', data['address'].lower())
            members.append(user_email)
        return members

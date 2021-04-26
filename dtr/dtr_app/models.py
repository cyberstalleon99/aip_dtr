import sqlite3
from datetime import datetime

import settings
db = sqlite3.connect(settings.DB_PATH)
cur = db.cursor()
# curr_date = datetime.now()

class Entry(object):
    curr_date = datetime.now()
    
    def __init__(self, name='', location='', date_in='', date_out='', work='', time_log=''):
        self.name = name
        self.location = location
        self.date_in = date_in
        self.date_out = date_out
        self.work = work
        self.time_log = time_log

    # @classmethod
    def create(self):
        qry = "INSERT into logbook (name, location, time_in, time_out, work) VALUES(?,?,?,?,?);"
        cur.execute(qry, (self.name, self.location, self.date_in, self.date_out, self.work))
        db.commit()

    # @classmethod
    def save(self, new=True):
        if new:
            self.create()

    @staticmethod
    def getAll():
        qry = "SELECT * FROM logbook"
        cur.execute(qry)
        query_result = cur.fetchall()
        result = [] 
        for item in query_result:
            entry = Entry(item[0], item[1], item[2], item[3], item[4], item[5])
            result.append(entry)

        return result

    @staticmethod
    def last_user_entry(name, time_in=True):
        curr_date = datetime.strftime(Entry.curr_date, '%Y-%m-%d')
        if time_in:
            cur.execute(
                "SELECT * FROM logbook WHERE name=? AND time_in != '' AND strftime('%Y-%m-%d', time_in)=?", (name, curr_date))
        else:
            cur.execute(
                "SELECT * FROM logbook WHERE name=? AND time_out != '' AND strftime('%Y-%m-%d', time_out)=?", (name, curr_date))

        try:
            query_result = cur.fetchall()[-1]
        except:
            return None
        else:
            if time_in == True:
                return datetime.strptime(query_result[3], '%Y-%m-%d %H:%M:%S.%f')
            elif time_in == False:
                return datetime.strptime(query_result[4], '%Y-%m-%d %H:%M:%S.%f')
            else:
                return None

class FleetEntry(object):

    def __init__(self, name='', unit='', date_in='', date_out='', purpose='', kmr='', time_log=''):
        self.name = name
        self.unit = unit
        self.date_in = date_in
        self.date_out = date_out
        self.purpose = purpose
        self.kmr = kmr
        self.time_log = time_log

    def create(self):
        qry = "INSERT INTO lugan (name, unit, time_in, time_out, purpose, kmr) VALUES(?,?,?,?,?,?);"
        cur.execute(qry, (self.name, self.unit, self.date_in, self.date_out, self.purpose, self.kmr))
        db.commit()
    
    def save(self, new=True):
        if new:
            self.create()

    @staticmethod
    def getAll():
        qry = "SELECT * FROM lugan"
        cur.execute(qry)
        query_result = cur.fetchall()
        result = [] 
        for item in query_result:
            entry = FleetEntry(item[0], item[1], item[2], item[3], item[4], item[5])
            result.append(entry)

        return result
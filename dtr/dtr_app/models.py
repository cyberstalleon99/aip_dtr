import sqlite3
from datetime import datetime, timedelta

import settings
from helpers.print import pretty_message, BColors
from helpers import excel, dates

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
    def getAllRange(date_from, date_to):
        qry = f"SELECT * FROM logbook WHERE time_log BETWEEN '{date_from}' and '{date_to}'"
        cur.execute(qry)
        result = [] 
        for item in cur:
            entry = Entry(item[1], item[2], item[3], item[4], item[5], item[6])
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

    @staticmethod
    def export_to_excel():
        date_from = input('From (YYYY-MM-DD). Press Q to exit: ')
        date_to = ''
        if dates.validate(date_from):
            date_to = input('  To (YYYY-MM-DD). Press Q to exit: ')
        else:
            if date_from == 'Q' or date_from == 'q':
                return
            else:
                pretty_message('Not a valid date. Date Format: YYYY-MM-DD', BColors.FAIL)
                Entry.export_to_excel()

        if dates.validate(date_to):
            excel.write('Logbook', Entry.getAllRange(date_from, datetime.strptime(date_to, "%Y-%m-%d") + timedelta(days=1)))
            pretty_message(f'Saved in {settings.DTR_EXTRACTS_PATH}', BColors.OKGREEN)
        else:
            if date_from == 'Q' or date_from == 'q':
                return
            else:
                pretty_message('Not a valid date. Date Format: YYYY-MM-DD', BColors.FAIL)
                Entry.export_to_excel()

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
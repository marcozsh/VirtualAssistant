import sqlite3
import re
import os
import subprocess

DATABASE = 'base.db'

def powershell(command): #allow to run powershell commands
    cmd = subprocess.run(["powershell", command], capture_output=True)
    return cmd.stdout

def connect_database(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print('conection failed')
    return conn

def insert_phrases(phrase, phrase_type):
    conn = connect_database(DATABASE)
    cur = conn.cursor()
    cur.executescript('INSERT INTO phrases (phrase, phrase_type) values(\'{}\', \'{}\')'.format(phrase, phrase_type)).fetchall()
    conn.close()
    return True

def initial_setup():
    conn = connect_database(DATABASE)
    cur = conn.cursor()
    try:
        cur.executescript(powershell('Get-Content sql.sql -Raw').decode('utf8')).fetchall()
        your_welcome_phrases = ['I’m happy to help', 'No worries', 'Not a problem',
                                'It was nothing', 'It is my pleasure', 'Anytime', 'I’m glad to help',
                                'No big deal']
        call_phrases = ['Yes?', 'How can I help?',
                        'Tell me', 'Qué weá querí', 'I am here sir']

        for i in range(len(your_welcome_phrases)):
            insert_phrases(your_welcome_phrases[i], 1)

        for i in range(len(call_phrases)):
            insert_phrases(call_phrases[i], 2)

        return True
    
    except sqlite3.OperationalError as e:
        print(e)
        return False



def get_name():
    conn = connect_database(DATABASE)
    cur = conn.cursor()
    try:

        cur.execute('SELECT name FROM IA')
        result = cur.fetchall()
        name = re.search('\'.*\'', str(result)).group(0).replace('\'', '')
        conn.close()
        return name, True

    except:
        return '', False

def set_name(name, flag): # if flag, then set name, else update the name
    conn = connect_database(DATABASE)
    cur = conn.cursor()
    if not flag:
        cur.executescript('BEGIN TRANSACTION; UPDATE IA SET name = \'{}\' where name = \'{}\'; COMMIT;'.format(
            name, get_name()[0])).fetchall()
    else:
        cur.executescript('BEGIN TRANSACTION; UPDATE IA SET name = \'{}\'; COMMIT;'.format(name)).fetchall()
    result = cur.execute('SELECT name FROM IA').fetchall()
    name = re.search('\'.*\'', str(result)).group(0).replace('\'', '')
    conn.close()
    return name



def get_phrases(phrase_type):
    conn = connect_database(DATABASE)
    cur = conn.cursor()
    phrase = cur.execute('SELECT phrase FROM phrases WHERE phrase_type = \'{}\''.format(phrase_type)).fetchall()
    conn.close()

    temp_list = []
    for i in range(len(phrase)):
        temp = str(phrase[i])
        temp = re.findall('\'.*\'', temp)
        temp_list.append(temp)
    phrase_list = []
    for i in range(len(temp_list)):
        temp = str(temp_list[i])
        temp = temp.replace('\'', '').replace('[','').replace(']','').replace('"','')
        phrase_list.append(temp)
    return phrase_list


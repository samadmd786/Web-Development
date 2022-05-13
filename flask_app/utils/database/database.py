from cProfile import run
import re
from select import select
import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow


class database:

    def __init__(self, purge=False):

        # Grab information from the configuration file
        self.database = 'db'
        self.host = '127.0.0.1'
        self.user = 'master'
        self.port = 3306
        self.password = 'master'
        self.tables = ['institutions', 'positions',
                       'experiences', 'skills', 'feedback', 'users']

        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption = {'oneway': {'salt': b'averysaltysailortookalongwalkoffashortbridge',
                                      'n': int(pow(2, 5)),
                                      'r': 9,
                                      'p': 1
                                      },
                           'reversible': {'key': '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                           }
        # -----------------------------------------------------------------------------

    def query(self, query="SELECT * FROM users", parameters=None):

        cnx = mysql.connector.connect(host=self.host,
                                      user=self.user,
                                      password=self.password,
                                      port=self.port,
                                      database=self.database,
                                      charset='latin1'
                                      )

        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path='flask_app/database/'):
        # print('I create and populate database tables.')

        table = ["skills", "experiences", "positions",
                 "institutions", "feedback" ]
        for k in table:
            self.query(f"""DROP table IF EXISTS {k};""")

        table = ["institutions", "positions",
                 "experiences", "skills", "feedback"]
        for table_name in table:
            query = open(data_path+"create_tables/"+table_name+".sql")
            file = query.read()
            self.query(file)

            file = open(data_path+"initial_data/"+table_name+".csv")
            csv_file = csv.reader(file)
            a = (next(csv_file, None))
            for i in csv_file:
                self.insertRows(table_name, [j.strip() for j in a], i)
        table = ["users", "leaderboard"]
        for table_name in table:
            query = open(data_path+"create_tables/"+table_name+".sql")
            file = query.read()
            self.query(file)

        self.getResumeData()

    def insertRows(self, table='table', columns=['x', 'y'], parameters=[['v11', 'v12'], ['v21', 'v22']]):
        # print('I insert things into the database.')
        column = " ".join(columns)
        column = column.replace(' ', ",")
        values = ''
        for i in parameters:
            values += "'"+i+"'"+','
        values = values.rstrip(',')
        query = f"""INSERT  INTO {table} ({column}) VALUES ({values}) """
        # print(query)
        self.query(query)

    def getResumeData(self):
        # Pulls data from the database to genereate data like this:

        resumeData = {}
        institutiondict = {}
        iter_inst = 0

        instQuery = self.query("SELECT * from institutions;")
        for row in instQuery:
            inst_temp_dict = {}
            iter_inst += 1
            inst_id = 0
            for key in row:
                if key == 'inst_id':
                    inst_id = row[key]
                else:
                    inst_temp_dict[key] = row[key]
            institutiondict[iter_inst] = inst_temp_dict
            posQuery = self.query(
                "SELECT * FROM positions WHERE positions.inst_id =%s;", [inst_id])
            pos_dict = {}
            iter_pos = 0
            for row in posQuery:
                pos_temp_dict = {}
                iter_pos += 1
                pos_id = 0
                for key in row:
                    if key == 'inst_id':
                        continue
                    elif key == 'position_id':
                        pos_id = row[key]
                    else:
                        pos_temp_dict[key] = row[key]
                pos_dict[iter_pos] = pos_temp_dict

                experienceQuery = self.query(
                    "SELECT * FROM experiences WHERE experiences.position_id =%s", [pos_id])
                experience_dict = {}
                iter_exp = 0
                for row in experienceQuery:
                    iter_exp += 1
                    exp_id = 0
                    exp_temp_dict = {}
                    for key in row:
                        if key == "position_id":
                            continue
                        elif key == "experience_id":
                            exp_id = row[key]
                        else:
                            exp_temp_dict[key] = row[key]
                    experience_dict[iter_exp] = exp_temp_dict
                exp_id = str(exp_id)
                skillQuery = self.query(
                    "SELECT * FROM skills WHERE skills.experience_id =%s", [exp_id])
                skill_dict = {}
                iter_skill = 0
                for row in skillQuery:
                    iter_skill += 1
                    skill_id = 0
                    skill_temp_dict = {}
                    for key in row:
                        if key == "experience_id":
                            continue
                        else:
                            skill_temp_dict[key] = row[key]
                    skill_dict[iter_skill] = skill_temp_dict

                    experience_dict['skills'] = skill_dict
                pos_dict['experiences'] = experience_dict
            institutiondict[iter_inst]['positions'] = pos_dict
        resumeData = institutiondict

        # print(resumeData.items())
        return resumeData

    def send_feedback(self, input):
        for i in input:
            print(input[i])
        name = ""
        email = ""
        comment = ""
        for i in input:
            if i == 'name':
                name = input[i]
            if i == 'email':
                email = input[i]
            if i == 'comment':
                comment = input[i]
        self.query(
            """INSERT INTO feedback (name, email, comment) VALUES (%s,%s,%s) """, [name, email, comment])
        # print(values)

    def get_feedback(self):
        data = self.query("SELECT * from feedback")
        self.get_leaderboard()
        return data

    def send_leaderboard(self,user, word,time, date):
        print(date)
        print(type(date))
        self.query(
            """INSERT INTO leaderboard (word, user, time, date) VALUES (%s,%s,%s,%s) """, [word, user, time,date])

        
    def get_leaderboard(self):
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        today_date = self.query("SELECT CURDATE() AS date;")
        # print(today_date)
        date = ""
        for i in today_date:
            # print(i["date"])
            date = i["date"]
        date = str(date)
        print(date)
        print(type(date))
        data = self.query("SELECT * from leaderboard where date = %s ORDER BY time",parameters=[date])
        # data = self.query("SELECT * from leaderboard ORDER BY time limit 5;")
        
        return data

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='user'):
        password = self.onewayEncrypt(password)
        response = self.query(
            """select exists(select * FROM users WHERE email=%s)""", parameters=[email])
        # print(response)
        for row in response:
            for exist in row.values():
                if exist == 0:
                    self.query(
                        """INSERT INTO users (email, password, role) VALUES (%s,%s,%s) """, [email, password, role])
                    return {'success': 1}
                else:
                    return {'success': 0}

    def authenticate(self, email='me@email.com', password='password'):
        password = self.onewayEncrypt(password)
        # print(enc_pass)
        # print("auth")
        response = self.query(
            """select exists(select * FROM users WHERE email=%s and password=%s)""", parameters=[email, password])
        for row in response:
            for exist in row.values():
                if exist == 1:
                    return {'success': 1}
                else:
                    return {'success': 0}

    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt=self.encryption['oneway']['salt'],
                                          n=self.encryption['oneway']['n'],
                                          r=self.encryption['oneway']['r'],
                                          p=self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string

    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])

        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message

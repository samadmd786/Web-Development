from ast import Delete
import queue
from select import select
import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import datetime


class database:

    def __init__(self, purge=False):

        # Grab information from the configuration file
        self.database = 'db'
        self.host = '127.0.0.1'
        self.user = 'master'
        self.port = 3306
        self.password = 'master'

    def query(self, query="SELECT CURDATE()", parameters=None):

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

    def about(self, nested=False):
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(
                row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(
                row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']
                                     ]['column_comment'] = row['column_comment']
            table_info[row['table']][row['column_name']
                                     ]['fk_column_name'] = row['fk_column_name']
            table_info[row['table']][row['column_name']
                                     ]['fk_table_name'] = row['fk_table_name']
            table_info[row['table']][row['column_name']
                                     ]['is_key'] = row['is_key']
            table_info[row['table']][row['column_name']
                                     ]['table'] = row['table']
        return table_info

    def createTables(self, purge=False, data_path='flask_app/database/'):
        # print('I create and populate database tables.')
       
        self.query("DROP table IF EXISTS skills")
        self.query("DROP table IF EXISTS experiences")
        self.query("DROP table IF EXISTS positions")
        self.query("DROP table IF EXISTS institutions")
        self.query("DROP table IF EXISTS feedback")

        query = open(data_path+"create_tables/institutions.sql")
        file = query.read()
        self.query(file)

        file = open(data_path+"initial_data/institutions.csv")
        csv_file = csv.reader(file)

        next(csv_file, None)
        for i in csv_file:
            self.insertRows('institutions', [
                            "inst_id", "type", "name", "department", "address", "city", "state", "zip"], i)

        # positions table
        query = open(data_path+"create_tables/positions.sql")
        file = query.read()
        self.query(file)

        file = open(data_path+"initial_data/positions.csv")
        csv_file = csv.reader(file)

        next(csv_file, None)
        for i in csv_file:
            self.insertRows('positions', [
                            "position_id", "inst_id", "title", "responsibilities", "start_date", "end_date"], i)

        # #experiences table
        query = open(data_path+"create_tables/experiences.sql")
        file = query.read()
        self.query(file)

        file = open(data_path+"initial_data/experiences.csv")
        csv_file = csv.reader(file)

        next(csv_file, None)
        for i in csv_file:
            self.insertRows('experiences', [
                            "experience_id", "position_id", "name", "description", "hyperlink", "start_date", "end_date"], i)

        # #skill table
        query = open(data_path+"create_tables/skills.sql")
        file = query.read()
        self.query(file)

        file = open(data_path+"initial_data/skills.csv")
        csv_file = csv.reader(file)

        next(csv_file, None)
        for i in csv_file:
            self.insertRows('skills', [
                            "skill_id", "experience_id", "name", "skill_level"], i)

        # feedback table
        query = open(data_path+"create_tables/feedback.sql")
        file = query.read()
        self.query(file)

        file = open(data_path+"initial_data/feedback.csv")
        csv_file = csv.reader(file)

        next(csv_file, None)
        for i in csv_file:
            self.insertRows('feedback', [
                            "comment_id", "name", "email", "comment"], i)
        
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

    def send_feedback(self,input):
        for i  in input:
            print(input[i])
        name = ""
        email = ""
        comment = ""
        for i in input:
            if i == 'name':
                name = input[i]
            if i == 'email':
                email =  input[i]
            if i == 'comment':
                comment =  input[i]
        self.query(
            """INSERT INTO feedback (name, email, comment) VALUES (%s,%s,%s) """,[name,email,comment])
        # print(values)
        
    def get_feedback(self):
        data = self.query("SELECT * from feedback")
        return data

        # return  {1:{'address': 'NULL',
        #             'city': 'East Lansing',
        #             'state': 'Michigan',
        #             'type': 'Academia',
        #             'zip': 'NULL',
        #             'department': 'Computer Science',
        #             'name': 'Michigan State University',
        #             'positions': {1: {'end_date': None,
        #                               'responsibilities': 'Teach classes; mostly NLP and Web design.',
        #                               'start_date': datetime.date(2020, 1, 1),
        #                               'title': 'Instructor',
        #                               'experiences': {1: {'description': 'Taught an introductory course ... ',
        #                                                   'end_date': None,
        #                                                   'hyperlink': 'https://gitlab.msu.edu',
        #                                                   'name': 'CSE 477',
        #                                                   'skills': {},
        #                                                   'start_date': None
        #                                                   },
        #                                               2: {'description': 'introduction to NLP ...',
        #                                                   'end_date': None,
        #                                                   'hyperlink': 'NULL',
        #                                                   'name': 'CSE 847',
        #                                                   'skills': {1: {'name': 'Javascript',
        #                                                                  'skill_level': 7},
        #                                                                2: {'name': 'Python',
        #                                                                    'skill_level': 10},
        #                                                                3: {'name': 'HTML',
        #                                                                    'skill_level': 9},
        #                                                                4: {'name': 'CSS',
        #                                                                    'skill_level': 5}},
        #                                                   'start_date': None
        #                                                   }
        #                                               }}}}}

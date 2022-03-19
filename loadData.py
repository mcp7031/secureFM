import sqlite3 as sql
import re
import csv
# from django.db import models
import random
import pandas as pd
import datetime

global fileName
   
fileName = 'D:\\Downloads\\MOCK_DATA.csv'

def connectSQLite():
   try:
     query = '''SELECT * FROM "ppt_company";'''
# Create a SQL connection to our SQLite database
     connect = sql.connect("db.sqlite3",
          detect_types=sql.PARSE_DECLTYPES |
          sql.PARSE_COLNAMES)
     cursor = connect.cursor()
     print("Connected to SQLite")
     cursor.execute(query)
     print("Set counted "+ str(cursor.description))
   except sql.Error as error:
       print("Failed to connect", error)
   finally:
      if (connect):
         connect.close()
         print("Connection closed")


class create_company:
 
    def __init__(self):
        self.max = 5
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):

        sqlInsert = "insert into 'ppt_company' ('company_id',\
                                                'companyName',\
                                                'tradeName',\
                                                'abn',\
                                                'account',\
                                                'contactL1',\
                                                'contactL2',\
                                                'contactL3'\
                                                ) values\n"  
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        for id in range(1, self.max):
            self.id_list.append(id)
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", '"
            sqlInsert += row['company_name']+"', '"
            sqlInsert += row['short_name']+"', '"
            sqlInsert += row['ip_address'].replace('.', '')+"', '"
            sqlInsert += str.strip(row['phone'], '()')+"', NULL, NULL, NULL),\n"
        print(sqlInsert)

    def get_id_list(self):
        return self.id_list

class create_nominal:

    def __init__(self):
        self.max = 200
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):
        loc = create_location()
        loc_id_list = loc.get_id_list()
        dc_list = ['M', 'C', 'H', 'HC', 'MMC']
        middleName_list = [' ', '  ', '    ']
        sqlInsert = "insert into 'ppt_nominal' ('nominal_id',\
                                                'location_id',\
                                                'dateCreated',\
                                                'dateBirth',\
                                                'lastName,\
                                                'firstName',\
                                                'middleName',\
                                                'driverLicense',\
                                                'driverClass',\
                                                'address1',\
                                                'address2'\
                                                ) values\n"
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        for id in range(1, self.max):
            row = self.rd.iloc[id]
            if id < 100:
                middleName_list.append(row['last_name'])
            self.id_list.append(id)
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1, 300))+", "
            sqlInsert += str(datetime.datetime.now())+", '"
            sqlInsert += row['date'][0:10]+"', '"
            sqlInsert += row['last_name']+"', '"
            sqlInsert += row['first_name']+"', '"
            sqlInsert += random.choice(middleName_list)+"', '"
            sqlInsert += row['phone'][-4:]+"', '"
            sqlInsert += random.choice(dc_list)+"', '"
            sqlInsert += row['street_addr']+"', '"
            sqlInsert += row['city']+"'),\n"
        print(sqlInsert)

    def get_id_list(self):
        return self.id_list

class create_location:

    def __init__(self):
        self.max = 300
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):

        costCentre_id_list = []
        bimm_id_list = []
        sqlInsert = "insert into 'ppt_location' ('location_id',\
                                                 'costCentre_id',\
                                                 'bimm_id',\
                                                 'locationCode',\
                                                 'locationName'\
                                                ) values\n"

        sqlInsert = re.sub(' +', ' ', sqlInsert)
        for id in range(1, self.max):
            self.id_list.append(id)
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1,100))+", "
            sqlInsert += str(random.randrange(1,400))+", '"
            sqlInsert += row['access_code']+"', '"
            sqlInsert += row['retail_dept']+"'),\n"
        print(sqlInsert)
        
    def get_id_list(self):
        return self.id_list

class create_bimm:

    def __init__(self):
        self.max = 400
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):

        bimm_id_list = []
        sqlInsert = "insert into 'ppt_bimm' ('bimm_id',\
                                             'bim_id',\
                                             'mongodb_id',\
                                             'description'\
                                             ) values\n"

        sqlInsert = re.sub(' +', ' ', sqlInsert)
        for id in range(1, self.max):
            self.id_list.append(id)
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1,400))+", "
            sqlInsert += row['mongo_id']+", '"
            sqlInsert += row['sentence']+"', '"
            sqlInsert += row['short_name']+"', '"
        print(sqlInsert)
        
    def get_id_list(self):
        return self.id_list

# open file for reading
def openDataFile():
    global filename
    companyName = []
    abn = []

    with open(fileName, "r", encoding='latin-1') as dFile:

        ndx = random.randrange(1, 1000)
    # read file as csv file
        csvReader = csv.reader(dFile)
        row1 = next(csvReader)
        print(row1)
#       for every row, print the row
        for row in csvReader:
            companyName.append(row[6])
            abn.append(row[5])
        dFile.close()
        print("company at ndx "+str(ndx)+" "+companyName[ndx]+" with abn "+abn[ndx]) 

connectSQLite()
comp = create_company()
comp.create_sql()
print(comp.get_id_list())
nominal = create_nominal()
nominal.create_sql()
location = create_location()
location.create_sql()

openDataFile()

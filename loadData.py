import sqlite3 as sql
import re
import csv
import random
import pandas as pd
import datetime
import mysql.connector
import const

global fileName
global WRITE_SCRIPT
   
fileName = 'D:\\Downloads\\MOCK_DATA.csv'
WRITE_SCRIPT = True

def sqlHeader():
   pass

def connectMySQL(host_name, user_name, user_password, db_name):
    db = None
    try:
        db = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
         )
        print("MySQL Database connection successful")
        myCursor = db.cursor()
    except mysql.connector.Error as err:
        print(f"Error: '{err}'")
        print(f"Error Code: '{err.errno}'")
        print(f"SQLSTATE '{err.sqlstate}'")
        print(f"Message '{err.msg}'")

    return db

def connectSQLite():
    try:
        query = '''SELECT * FROM "ppt_company";'''
# Create a SQL connection to our SQLite database
        db = sql.connect("db.sqlite3",
            detect_types=sql.PARSE_DECLTYPES |
            sql.PARSE_COLNAMES)
        liteCursor = db.cursor()
    except sql.Error as err:
        print("Failed to connect", err)
    finally:
        print("Connected to SQLite")
        liteCursor.execute(query)
        print("Set counted "+ str(liteCursor.description))

    return db

#  
# note to myself: where is the documentation on the attributes
# of the return value of pd.to_datetime??  I've checked the pandas
# docs. Kite gives all kinds of attributes some of which like count()
# are not actually an attribute. But where are they documented? Where
# is the value attribute documented?
#   
def random_date():
    start = pd.to_datetime('2015-01-01')
    end = pd.to_datetime('2022-01-31')
#    print(f"start time: '{start.time}'")
    startU = start.value//10**9
    endU = end.value//10**9
    return pd.to_datetime(random.randint(startU, endU), unit='s')

class create_company:
 
    def __init__(self):
        self.max = const.CO_MAX
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
                                                ) values \n"  
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", '"
            sqlInsert += row['company_name']+"', '"
            sqlInsert += row['short_name']+"', '"
            sqlInsert += row['ip_address'].replace('.', '')+"', '"
            sqlInsert += str.strip(row['phone'], '()')+"), "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+", "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+", "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+")"+lc
        print(sqlInsert)

    def get_id_list(self):
        return self.id_list

class create_costCentre:
 
    def __init__(self):
        self.max = const.CC_MAX 
        self.id_list = []
        self.company_id_list = []
        self.nominal_id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(10)

    def create_sql(self):
        sqlInsert = "insert into 'ppt_costCentre ' ('costCentre_id',\
                                                'company',\
                                                'costName',\
                                                'costAccount',\
                                                'contactL1',\
                                                'contactL2',\
                                                'contactL3'\
                                                ) values \n"  
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n" 
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            row = self.rd.iloc[id]
            company_id = random.choice(self.company_id_list)
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(company_id)+", '"
            sqlInsert += row['fake_company']+"', '"
            sqlInsert += str.strip(row['phone'], '()')+"', "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+", "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+", "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+")"+lc
        print(sqlInsert)

    def set_max(self, n):
        self.max = n

    def get_max(self):
        return self.max

    def set_company_list(self, co_list):
        self.company_id_list = co_list

    def get_company_list(self):
        return self.company_id_list

    def get_id_list(self):
        return self.id_list

class create_nominal:

    def __init__(self):
        self.max = const.NOM_MAX 
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)
    def create_sql(self):
        dc_list = ['M', 'C', 'H', 'HC', 'MMC']
        middleName_list = [' ', '  ', '    ']
        sqlInsert = "insert into 'ppt_nominal' ('nominal_id',\
                                                'costCentre',\
                                                'location',\
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
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            row = self.rd.iloc[id]
            if id < 100:
                middleName_list.append(row['last_name'])
            self.id_list.append(id)
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1, const.CC_MAX))+", "
            sqlInsert += str(random.randrange(1, const.LOC_MAX))+", "
            sqlInsert += str(random_date())+", '"
            sqlInsert += row['date'][0:10]+"', '"
            sqlInsert += row['last_name']+"', '"
            sqlInsert += row['first_name']+"', '"
            sqlInsert += random.choice(middleName_list)+"', '"
            sqlInsert += row['phone'][-4:]+"', '"
            sqlInsert += random.choice(dc_list)+"', '"
            sqlInsert += row['street_addr']+"', '"
            sqlInsert += row['city']+"')"+lc
        print(sqlInsert)

    def get_id_list(self):
        return self.id_list

class create_location:

    def __init__(self):
        self.max = const.LOC_MAX
        self.id_list = []
        self.cc_id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):

        costCentre_id_list = []
        bimm_id_list = []
        sqlInsert = "insert into 'ppt_location' ('location_id',\
                                                 'costCentre',\
                                                 'locationCode'\
                                                 'description'\
                                                ) values\n"

        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1, const.CC_MAX))+", '"
            sqlInsert += row['access_code']+"', '"
            sqlInsert += row['retail_dept']+"')"+lc
        print(sqlInsert)
        
    def set_max(self, n):
        self.max = n

    def get_max(self):
        return self.max

    def set_costCentre_list(self, cc_list):
        self.cc_id_list = cc_list

    def get_costCentre_list(self):
        return self.cc_id_list

    def get_id_list(self):
        return self.id_list

# 
# BIMMbyLocation is a M:N relation between location and BIMM
# it also contains other (user supplied) information to help explain why one
# relation is different from another similar one.  It would probably be an
# interesting report to identify similar relationships, and/or provide some
# intelligence to assist in the differentiation.
#  
class create_bimmbylocation:
    def __init__(self):
        self.max = const.LOC_MAX * 4
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):

        bimm_id_list = []
        sqlInsert = "insert into 'ppt_bimmbylocation' ('id',\
                                                       'location_id',\
                                                       'bimm_id',\
                                                       'dateModified',\
                                                       'note'\
                                                       ) values\n"
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1,const.LOC_MAX))+", "
            sqlInsert += str(random.randrange(1,const.BIMM_MAX))+", '"
            sqlInsert += str(random_date())+"', '"
            sqlInsert += row['sentence']+"')"+lc
        print(sqlInsert)
        
    def get_id_list(self):
        return self.id_list

# serviceLog has 1:M relationship with BIMM, although BIMM has a M:N with BIM
# it may be argued that this makes little sense however, in practical terms
# the BIMM is the management entity and a more complicated structure would
# entail more user level administration and probably unnecessary complexity
class create_serviceLog:
    def __init__(self):
        self.max = const.LOG_MAX 
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):

        service_id_list = []
        sqlInsert = "insert into 'ppt_servicelog' ('servicelog_id',\
                                                   'logDate',\
                                                   'note',\
                                                   'bimm_id',\
                                                   'who_id'\
                                                   ) values\n"
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", '"
            sqlInsert += str(random_date())+"', '"
            sqlInsert += row['sentence']+"', "
            sqlInsert += str(random.randrange(1,const.BIMM_MAX))+", "
            sqlInsert += str(random.randrange(1,const.NOM_MAX))+")"+lc
        print(sqlInsert)
        
    def get_id_list(self):
        return self.id_list

#
# haven't adequately settled what this object is going to hold
# there should be some documents and methods concerning the
# management of an asset
#
class create_bimm:

    def __init__(self):
        self.max = const.BIMM_MAX 
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):

        bimm_id_list = []
        sqlInsert = "insert into 'ppt_bimm' ('bimm_id',\
                                             'bim_id',\
                                             'name'\
                                             'description'\
                                             'purchaseDate'\
                                             'warranty'\
                                             'note'\
                                             'mtbf'\
                                             'hoursToDate'\
                                             'safety'\
                                             'manual'\
                                             'iotURL'\
                                             'iotDevice'\
                                             'msds'\
                                             ) values\n"

        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1,const.BIM_MAX))+", '"
            sqlInsert += row['short_name']+"', '"
            sqlInsert += row['sentence']+"', '"
            sqlInsert += str(random_date())+"', "
            sqlInsert += row['mongo_id']+", '"
            sqlInsert += row['sentence']+"', "
            sqlInsert += str(random.randrange(5000, 9999999))+", "
            sqlInsert += str(random.randrange(100, 9999999))+", "
            sqlInsert += row['mongo_id']+", "
            sqlInsert += row['mongo_id']+", '"
            sqlInsert += "https://"+row['short_name'].replace(" ","_")+"/"+row['mongo_id']+"', '"
            sqlInsert += row['short_name'].replace(" ","_")+row['mongo_id']+"', "
            sqlInsert += row['mongo_id']+")"+lc
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

if WRITE_SCRIPT:
   conLite = connectSQLite()
   sqlScriptFile = open("sqlScript.txt", "w+")
   conMy = connectMySQL("localhost", "dca", "Katie@1992", "ppt")

comp = create_company()
comp.create_sql()
print(comp.get_id_list())
cc = create_costCentre()
cc.set_company_list(comp.get_id_list())
cc.set_max(4)
cc.create_sql()
print(cc.get_id_list())
nominal = create_nominal()
nominal.create_sql()
location = create_location()
location.create_sql()
BIMMbyLoc = create_bimmbylocation()
BIMMbyLoc.create_sql()
sl = create_serviceLog()
sl.create_sql()
BIMM = create_bimm()
BIMM.create_sql()

if WRITE_SCRIPT:
  sqlScriptFile.close()
  conMy.cursor().close()
  conMy.close()
  conLite.cursor().close()
  conLite.close()
# openDataFile()

import sqlite3 as sql
import re
import csv
import random
import pandas as pd
import datetime
import mysql.connector
import const
from pymongo import MongoClient
from djongo import models as mongo
import services
import locations

global fileName, WRITE_SCRIPT
   
fileName = 'D:\\Downloads\\MOCK_DATA.csv'
WRITE_SCRIPT = True

def sqlHeader():
   pass

class Blob(mongo.Model):
    name = mongo.CharField(max_length=100)
    tagline = mongo.TextField()
    
    class Meta:
        abstract = True

#
# connect to mySQL
#
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
    except mysql.connector.Error as err:
        print(f"Error: '{err}'")
        print(f"Error Code: '{err.errno}'")
        print(f"SQLSTATE '{err.sqlstate}'")
        print(f"Message '{err.msg}'")

    return db

#
# connect to SQLite
#
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
# connect to MongoDB
#
def connectMongo(db_name, host, port, username, password):
    client = MongoClient(host=host,
                         port=int(port),
                         username=username,
                         password=password
                        )
    db_handle = client[db_name]
    return db_handle, client

def get_mongo_collection(db_handle, collection_name):
    return db_handle[collection_name]

#  
# note to myself: where is the documentation on the attributes
# of the return value of pd.to_datetime??  I've checked the pandas
# docs. Kite gives all kinds of attributes some of which like count()
# are not actually an attribute. But where are they documented? Where
# is the value attribute documented?
#   
def random_date(flag):
    if (flag == 0):
      start = pd.to_datetime('2015-01-01')
      end = pd.to_datetime('2022-01-31')
    if (flag == 1):
      start = pd.to_datetime('1968-01-01')
      end = pd.to_datetime('2002-01-31')
#    print(f"start time: '{start.time}'")
    startU = start.value//10**9
    endU = end.value//10**9
#    dt = random.randint(startU, endU)
#    return  pd.to_datetime(dt, format='%Y%m%d', errors='coerce')
    return pd.to_datetime(random.randint(startU, endU), unit='s')

def isEveryOther(time):
   return (random.randrange(1,100) % time == 0)

class create_company:
 
    def __init__(self):
        self.max = const.CO_MAX
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):
        sqlInsert = "insert into ppt_company (company_id,\
                                                compName,\
                                                tradeName,\
                                                abn,\
                                                account,\
                                                contactL1_id,\
                                                contactL2_id,\
                                                contactL3_id\
                                                ) values \n"  
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            row = self.rd.iloc[id]
            abn = row['ip_address'].replace('.','')
            sqlInsert += "("+str(id)+", '"
            sqlInsert += row['company_name']+"', '"
            sqlInsert += row['short_name']+"', '"
            sqlInsert += abn[1:8]+"', '"
            sqlInsert += str.strip(row['phone'], '()')+"', "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+", "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+", "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+")"+lc
        print(sqlInsert)
        return sqlInsert

    def get_id_list(self):
        return self.id_list

class create_services:
    def __init__(self):
      self.id_list = []
      self.SER_MAX = len(services.TRADES)
      res = self.sCode, self.serv = random.choice(list(services.TRADES.items()))
      self.max = len(services.TRADES)

    def create_sql(self):
        sqlInsert = "insert into ppt_services (services_id,\
                                               serviceCode,\
                                               serviceName\
                                                ) values \n"  
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n" 
        id = 1
        for sCode in services.TRADES:
            if (id == self.max):
                lc = ";\n"
            self.id_list.append(id)
            sqlInsert += "("+str(id)+", '"
            sqlInsert += sCode+"', '"
            sqlInsert += services.TRADES[sCode]+"')"+lc
            id += 1
        print(sqlInsert)
        return sqlInsert

    def get_service(self):
        return self.serv

    def get_serviceCode(self):
        return self.sCode
#
# 
class create_accessGroups:
    def __init__(self):
      self.id_list = []
      self.max = int(const.LOC_MAX/2)
      df = pd.read_csv(fileName)
      self.rd = df.sample(self.max)

    def create_sql(self):
        sqlInsert = "insert into ppt_accessGroups (accessGroup_id,\
                                                   groupCode,\
                                                   groupName,\
                                                   accessLevel\
                                                ) values \n"  
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n" 
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", '"
            sqlInsert += row['access_code']+"', '"
            sqlInsert += row['street name']+"', "
            sqlInsert += str(random.randrange(1, 6))+")"+lc
        print(sqlInsert)
        return sqlInsert

class create_locationGroupAccess:
    def __init__(self):
      self.id_list = []
      self.max = const.LOC_MAX

    def create_sql(self):
        sqlInsert = "insert into ppt_locationGroupAccess (locationGroupAccess_id,\
                                                          location_id,\
                                                          accessGroup_id\
                                                          ) values \n"  
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n" 
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1, const.LOC_MAX))+", "
            sqlInsert += str(random.randrange(1, int(const.LOC_MAX/2)))+")"+lc
        print(sqlInsert)
        return sqlInsert

class create_nominalGroupAccess:
    def __init__(self):
      self.id_list = []
      self.max = const.TEN_MAX

    def create_sql(self):
        sqlInsert = "insert into ppt_nominalGroupAccess (nominalGroupAccess_id,\
                                                         nominal_id,\
                                                         accessGroup_id\
                                                         ) values \n"  
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n" 
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1, const.TEN_MAX))+", "
            sqlInsert += str(random.randrange(1, int(const.LOC_MAX/2)))+")"+lc
        print(sqlInsert)
        return sqlInsert

class create_costCentre:
 
    def __init__(self):
        self.max = const.CC_MAX 
        self.id_list = []
        self.company_id_list = []
        self.nominal_id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(10)

    def create_sql(self):
        sqlInsert = "insert into ppt_costCentre  (costCentre_id,\
                                                  company_id,\
                                                  costName,\
                                                  costAccount,\
                                                  contactL1_id,\
                                                  contactL2_id,\
                                                  contactL3_id\
                                                ) values \n"  
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n" 
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            row = self.rd.iloc[id]
            company_id = str(random.randrange(1, const.CO_MAX))
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(company_id)+", '"
            sqlInsert += row['fake_company'].replace("'", "`")+"', '"
            sqlInsert += str.strip(row['phone'], '()')+"', "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+", "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+", "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+")"+lc
        print(sqlInsert)
        return sqlInsert

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
        sqlInsert = "insert into ppt_nominal (nominal_id,\
                                              costCentre_id,\
                                              location_id,\
                                              dateCreated,\
                                              createdBy_id,\
                                              dateBirth,\
                                              lastName,\
                                              firstName,\
                                              middleName,\
                                              driverLicense,\
                                              driverClass,\
                                              address1,\
                                              address2,\
                                              phone,\
                                              mobile\
                                               ) values\n"
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            row = self.rd.iloc[id]
            if id < 100:
                middleName_list.append(row['last_name'].replace("'", "`"))
            self.id_list.append(id)
            incident_id=' '
            if (isEveryOther(3)):
                incident_id = create_nominalIncident(row)
            safety_id = create_nominalSafety(row)
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1, const.CC_MAX))+", "
            sqlInsert += str(random.randrange(1, const.LOC_MAX))+", '"
            sqlInsert += str(random_date(0))+"', "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+", '"
            sqlInsert += str(random_date(1))+"', '"
            sqlInsert += row['last_name'].replace("'", "`")+"', '"
            sqlInsert += row['first_name'].replace("'", "`")+"', '"
            sqlInsert += random.choice(middleName_list)+"', '"
            sqlInsert += row['phone'][-4:]+"', '"
            sqlInsert += random.choice(dc_list)+"', '"
            sqlInsert += row['street_addr']+"', '"
            sqlInsert += row['city']+"', "
            sqlInsert += row['phone']+", " 
            sqlInsert += row['phone'].replace('-','')+")" +lc
        print(sqlInsert)
        return sqlInsert

    def get_id_list(self):
        return self.id_list

class create_personnel:

    def __init__(self):
        self.max = const.PER_MAX 
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):
        sqlInsert = "insert into ppt_personnel (nominal_ptr_id,\
                                                 dateStart,\
                                                 dateModified,\
                                                 contractor_id,\
                                                 services_id\
                                                 ) values\n"
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", '"
            sqlInsert += str(random_date(1))+"', '"
            sqlInsert += str(random_date(1))+"', "
            sqlInsert += str(random.randrange(1, const.CON_MAX))+", "
            sqlInsert += str(random.randrange(1, 40))+")"+lc
        print(sqlInsert)
        return sqlInsert
    
class create_documents:

    def __init__(self):
        self.max = const.NOM_MAX+const.PER_MAX
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):
        sqlInsert = "insert into ppt_documents (document_id,\
                                                nominal_id,\
                                                docName,\
                                                docDesc,\
                                                document\
                                                 ) values\n"
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            row = self.rd.iloc[id]
            docName = row['short_name']
            document_id = create_document(row, docName)
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+", '"
            sqlInsert += row['short_name']+"', '"
            sqlInsert += row['sentence']+"', '"
            sqlInsert += str(document_id)+"')"+lc
        print(sqlInsert)
        return sqlInsert

# create  document
#
def create_document(row, docName):
    document = {
            "file_title" : docName,
            "file_URL" : "https://"+row['short_name'].replace(" ","_")+"/"+row['mongo_id'][1:6],
            "uploaded_by" : row['short_name'][1:5],
            "created_at" : random_date(0),
            "updated_by" : row['email'],
            "company" : row['company_name'],
            "tags" : [
                { "name" : row['short_name'] },
                { "synopsis" : row['sentence'] },
                ],
            "version" : "<version>"
            }
    res = db_collection.insert_one(document)
#    print(document)
    return res.inserted_id

class create_tenant:

    def __init__(self):
        self.max = const.NOM_MAX 
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):
        sqlInsert = "insert into ppt_tenant (nominal_ptr_id,\
                                             companyName,\
                                             services_id,\
                                             lease,\
                                             base,\
                                             percentage1,\
                                             percentage2,\
                                             percentage3,\
                                             salesLimit1,\
                                             salesLimit2,\
                                             salesLimit3\
                                             ) values\n"
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(const.CON_MAX, self.max):
            if (id == self.max-1):
                lc = ";\n"
            row = self.rd.iloc[id]
            lease_id = create_lease(row)
            sqlInsert += "("+str(id)+", '"
            sqlInsert += row['fake_company'].replace("'", "`")+"', "
            sqlInsert += str(random.randrange(1, 40))+", '"
            sqlInsert += str(lease_id)+"', " 
            sqlInsert += str(random.randrange(10001, 600000))+", "
            sqlInsert += str(random.randrange(5, 10))+", "
            sqlInsert += str(random.randrange(2, 4))+", "
            sqlInsert += str(random.randrange(1, 3))+", "
            sqlInsert += str(random.randrange(1000, 10000))+", "
            sqlInsert += str(random.randrange(10001, 600000))+", "
            sqlInsert += str(random.randrange(600001, 9999999))+")"+lc
        print(sqlInsert)
        return sqlInsert

class create_contractor:

    def __init__(self):
        self.max = const.CON_MAX 
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):
        sqlInsert = "insert into ppt_contractor (contractor_id,\
                                                 services_id,\
                                                 dateCreated,\
                                                 dateModified,\
                                                 companyName,\
                                                 companyNumber,\
                                                 companyPhone,\
                                                 contactL1_id,\
                                                 contactL2_id,\
                                                 contactL3_id\
                                                 ) values\n"
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1, 40))+", '"
            sqlInsert += str(random_date(0))+"', '"
            sqlInsert += str(random_date(1))+"', '"
            sqlInsert += row['fake_company'].replace("'", "`")+"', '"
            sqlInsert += row['ip_address'].replace('.', '')[1:8]+"', '"
            sqlInsert += row['phone']+"', "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+", "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+", "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+")"+lc
        print(sqlInsert)
        return sqlInsert
    

    def get_id_list(self):
        return self.id_list

class create_retailLocation:

    def __init__(self):
        self.max = const.LOC_MAX
        self.id_list = []
        self.cc_id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):

        costCentre_id_list = []
        bimm_id_list = []
        sqlInsert = "insert into ppt_location (location_id,\
                                               costCentre_id,\
                                               locationCode,\
                                               description,\
                                               length,\
                                               width\
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
            sqlInsert += row['retail_dept']+"', "
            sqlInsert += str(random.randrange(24,300))+", "
            sqlInsert += str(random.randrange(18,300))+")"+lc
        print(sqlInsert)
        return sqlInsert

        
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

class create_officeLocation:

    def __init__(self):
        self.max = const.LOC_MAX*2
        self.id_list = []
        self.cc_id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):

        costCentre_id_list = []
        bimm_id_list = []
        sqlInsert = "insert into ppt_location (location_id,\
                                               costCentre_id,\
                                               locationCode,\
                                               description,\
                                               length,\
                                               width\
                                               ) values\n"

        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(const.LOC_MAX+1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1, const.CC_MAX))+", '"
            sqlInsert += row['access_code']+str(random.randrange(1,60))+"', '"
            sqlInsert += random.choice(list(locations.LOC))+"', "
            sqlInsert += str(random.randrange(34,300))+", "
            sqlInsert += str(random.randrange(28,300))+")"+lc
        print(sqlInsert)
        return sqlInsert

        
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
        sqlInsert = "insert into ppt_bimmbylocation (id,\
                                                     location_id,\
                                                     bimm_id,\
                                                     dateModified,\
                                                     note\
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
            sqlInsert += str(random_date(0))+"', '"
            sqlInsert += row['sentence']+"')"+lc
        print(sqlInsert)
        return sqlInsert
        
    def get_id_list(self):
        return self.id_list

# 
# BIMMbyBIM is a M:N relation between BIMM and BIM
# it also contains other (user supplied) information to help explain why one
# relation is different from another similar one.
#  
class create_BIMMbyBIM:
    def __init__(self):
        self.max = const.LOC_MAX * 4
        self.id_list = []
        df = pd.read_csv(fileName)
        self.rd = df.sample(self.max)

    def create_sql(self):

        bimm_id_list = []
        sqlInsert = "insert into ppt_bimmbybim (id,\
                                                bim_id,\
                                                bimm_id,\
                                                dateModified,\
                                                note\
                                                ) values\n"
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", "
            sqlInsert += str(random.randrange(1,const.BIM_MAX))+", "
            sqlInsert += str(random.randrange(1,const.BIMM_MAX))+", '"
            sqlInsert += str(random_date(0))+"', '"
            sqlInsert += row['sentence']+"')"+lc
        print(sqlInsert)
        return sqlInsert
        
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
        sqlInsert = "insert into ppt_servicelog (servicelog_id,\
                                                 logDate,\
                                                 note,\
                                                 bimm_id,\
                                                 who_id\
                                                 ) values\n"
        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            row = self.rd.iloc[id]
            sqlInsert += "("+str(id)+", '"
            sqlInsert += str(random_date(0))+"', '"
            sqlInsert += row['sentence']+"', "
            sqlInsert += str(random.randrange(1,const.BIMM_MAX))+", "
            sqlInsert += str(random.randrange(1,const.NOM_MAX))+")"+lc
        print(sqlInsert)
        return sqlInsert
        
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
        sqlInsert = "insert into ppt_bimm (bimm_id,\
                                           name,\
                                           description,\
                                           purchaseDate,\
                                           warranty,\
                                           note,\
                                           mtbf,\
                                           hoursToDate,\
                                           safety,\
                                           manual,\
                                           iotURL,\
                                           iotDevice,\
                                           msds,\
                                           reviewedDate,\
                                           reviewedBy_id\
                                           ) values\n"

        sqlInsert = re.sub(' +', ' ', sqlInsert)
        lc = ",\n"
        for id in range(1, self.max):
            if (id == self.max-1):
                lc = ";\n"
            self.id_list.append(id)
            row = self.rd.iloc[id]
            warranty_id = create_warranty(row)
            manual_id = create_manual(row)
            safety_id = create_safety(row)
            msds_id = create_msds(row)
            sqlInsert += "("+str(id)+", '"
            sqlInsert += row['short_name']+"', '"
            sqlInsert += row['sentence']+"', '"
            sqlInsert += str(random_date(0))+"', '"
            sqlInsert += str(warranty_id)+"', '"
            sqlInsert += row['sentence']+"', "
            sqlInsert += str(random.randrange(5000, 9999999))+", "
            sqlInsert += str(random.randrange(100, 9999999))+", '"
            sqlInsert += str(safety_id)+"','" 
            sqlInsert += str(manual_id)+"', '" 
            sqlInsert += "https://"+row['short_name'].replace(" ","_")+"/"+row['mongo_id']+"', '"
            sqlInsert += row['short_name'].replace(" ","_")+row['mongo_id']+"', '"
            sqlInsert += str(msds_id)+"', '"
            sqlInsert += str(random_date(0))+"', "
            sqlInsert += str(random.randrange(1, const.NOM_MAX))+")"+lc
        print(sqlInsert)
        return sqlInsert
        
    def get_id_list(self):
        return self.id_list

# create lease agreement document
#
def create_lease(row):
    lease = {
            "file_title" : "lease",
            "file_URL" : "https://"+row['short_name'].replace(" ","_")+"/"+row['mongo_id'][1:6],
            "uploaded_by" : row['email'],
            "created_at" : random_date(0),
            "updated_by" : row['email'],
            "department" : row['retail_dept'],
            "tags" : [
                { "name" : row['short_name'] },
                { "name" : "<tag2>" }
                ],
            "version" : "<version>"
            }
    res = db_collection.insert_one(lease)
    return res.inserted_id

# create warranty document
#
def create_warranty(row):
    warranty = {
            "file_title" : "warranty",
            "file_URL" : "https://"+row['short_name'].replace(" ","_")+"/"+row['mongo_id'][1:6],
            "uploaded_by" : row['email'],
            "created_at" : random_date(0),
            "updated_by" : row['email'],
            "department" : row['retail_dept'],
            "tags" : [
                { "name" : row['short_name'] },
                { "name" : "<tag2>" }
                ],
            "version" : "<version>"
            }
    res = db_collection.insert_one(warranty)
#    print(warranty)
    return res.inserted_id
#    return row['mongo_id']

# create manual document
#
def create_manual(row):
    manual = {
            "file_title" : "operating/service manual",
            "file_URL" : "https://"+row['short_name'].replace(" ","_")+"/"+row['mongo_id'][1:6],
            "uploaded_by" : row['short_name'][1:5],
            "created_at" : random_date(0),
            "updated_by" : row['email'],
            "company" : row['company_name'],
            "tags" : [
                { "name" : row['short_name'] },
                { "synopsis" : row['sentence'] },
                ],
            "version" : "<version>"
            }
    res = db_collection.insert_one(manual)
#    print(manual)
    return res.inserted_id

# create BIMM safety document
#
def create_safety(row):
    safety = {
            "file_title" : "safety procedure manual",
            "file_URL" : "https://"+row['short_name'].replace(" ","_")+"/"+row['mongo_id'][1:6],
            "uploaded_by" : row['short_name'][1:5],
            "created_at" : random_date(0),
            "updated_by" : row['email'],
            "department" : row['retail_dept'],
            "tags" : [
                { "name" : "<tag1>" },
                { "name" : "<tag2>" }
                ],
            "version" : 1.0
            }
    res = db_collection.insert_one(safety)
    return res.inserted_id

# create nominal safety document (root of list)
#
def create_nominalSafety(row):
    safety = {
            "file_title" : "Nominal safety documentation",
            "file_URL" : "https://"+row['short_name'].replace(" ","_")+"/"+row['mongo_id'][1:6],
            "uploaded_by" : row['email'],
            "created_at" : random_date(0),
            "updated_by" : row['email'],
            "department" : row['retail_dept'],
            "tags" : [
                { "orientation" : "<tag1>" },
                { "next document" : "<tag2>" }
                ],
            "version" : 1.0
            }
    res = db_collection.insert_one(safety)
    return res.inserted_id

# create nominal incident document (root of list)
#
def create_nominalIncident(row):
    incident = {
            "file_title" : "Nominal incident documentation",
            "file_URL" : "https://"+row['short_name'].replace(" ","_")+"/"+row['mongo_id'][1:6],
            "uploaded_by" : row['email'],
            "created_at" : random_date(0),
            "updated_by" : row['email'],
            "department" : row['retail_dept'],
            "tags" : [
                { "incident" : "<tag1>" },
                { "next document" : "<tag2>" }
                ],
            "version" : 1.0
            }
    res = db_collection.insert_one(incident)
    return res.inserted_id

# create msds document
#
def create_msds(row):
    msds = {
            "file_title" : "material safety data sheet",
            "file_URL" : "https://"+row['short_name'].replace(" ","_")+"/"+row['mongo_id'][1:6],
            "uploaded_by" : row['email'],
            "created_at" : random_date(0),
            "updated_by" : row['email'],
            "department" : row['retail_dept'],
            "tags" : [
                { "name" : row['short_name']},
                { "name" : "<tag2>" }
                ],
            "version" : "<version>"
            }
    res = db_collection.insert_one(msds)
    return res.inserted_id


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
   mySQLconnection = connectMySQL("localhost", "dca", "Katie@1992", "ppt")
   db_handle, client = connectMongo("ppt_db", "192.168.8.110", 27017, "admin", "Katie@1992")
   db_collection = get_mongo_collection(db_handle,"ppt documents")

comp = create_company()
res = comp.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_company;")
    cursor.execute(res)
    mySQLconnection.commit()
cc = create_costCentre()
res = cc.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_costcentre;")
    cursor.execute(res)
    mySQLconnection.commit()
nominal = create_nominal()
res = nominal.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_nominal;")
    cursor.execute(res)
    mySQLconnection.commit()
document = create_documents()
res = document.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_documents;")
    cursor.execute(res)
    mySQLconnection.commit()
personnel = create_personnel()
res = personnel.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_personnel;")
    cursor.execute(res)
    mySQLconnection.commit()
tenant = create_tenant()
res = tenant.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_tenant;")
    cursor.execute(res)
    mySQLconnection.commit()
location = create_retailLocation()
res = location.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_location;")
    cursor.execute(res)
    mySQLconnection.commit()
location = create_officeLocation()
res = location.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute(res)
    mySQLconnection.commit()
BIMMbyLoc = create_bimmbylocation()
res = BIMMbyLoc.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_BIMMbylocation;")
    cursor.execute(res)
    mySQLconnection.commit()
BIMMbyBIM = create_BIMMbyBIM()
res = BIMMbyBIM.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_BIMMbyBIM;")
    cursor.execute(res)
    mySQLconnection.commit()
sl = create_serviceLog()
res = sl.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_servicelog;")
    cursor.execute(res)
    mySQLconnection.commit()
BIMM = create_bimm()
res = BIMM.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_BIMM;")
    cursor.execute(res)
    mySQLconnection.commit()
service = create_services()
res = service.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_services;")
    cursor.execute(res)
    mySQLconnection.commit()
contr = create_contractor()
res = contr.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_contractor;")
    cursor.execute(res)
    mySQLconnection.commit()
accessG = create_accessGroups()
res = accessG.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_accessgroups;")
    cursor.execute(res)
    mySQLconnection.commit()
locAccess = create_locationGroupAccess()
res = locAccess.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_locationgroupaccess;")
    cursor.execute(res)
    mySQLconnection.commit()
nomAccess = create_nominalGroupAccess()
res = nomAccess.create_sql()
with mySQLconnection.cursor() as cursor:
    cursor.execute("set foreign_key_checks = 0;")
    cursor.execute("truncate ppt_nominalgroupaccess;")
    cursor.execute(res)
    mySQLconnection.commit()

if WRITE_SCRIPT:
  sqlScriptFile.close()
  mySQLconnection.cursor().close()
  mySQLconnection.close()
  conLite.cursor().close()
  conLite.close()
# openDataFile()

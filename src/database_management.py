# usage example:
#import database_management as db_class
#import pandas as pd

#db = db_class.database_management()
#db.get_connection()
#res = db.query('SELECT * FROM table_name')


## insert example
# data = {'timestamp':[1565000322], 'var1':[3], 'va2':[3]}
# df = pd.DataFrame(data)
# headers = ['timestamp','var1','var2']
# db.insert('table_name',headers,df)
# db.close()


import psycopg2
import pymssql
import yaml
import pandas as pd
import math

class database_management:

    def __init__(self):
        self.isconnected = False
        self.conn = None
        self.host = None
        self.user = None
        self.password = None
        self.dbname = None
        self.port = None
        self.engine = None
        self.curs = None
        self.dataframe = None


    def get_connection(self):
        with open("config.yaml", 'r') as stream:
            config = yaml.safe_load(stream)
            #print(config)
        #return config
        self.host = config['database']['host']
        self.user = config['database']['user']
        self.password = config['database']['password']
        self.dbname = config['database']['dbname']
        self.port = config['database']['port']
        self.engine = config['database']['engine']
        self.dataframe = config['database']['dataframe']
        try:
            if self.engine=='postgres':
                self.conn = psycopg2.connect(host=self.host, database=self.dbname, user=self.user,password=self.password,port=self.port,connect_timeout=3)
                self.curs = self.conn.cursor()
                self.isconnected = True
            elif self.engine=='mssql':
                self.conn = pymssql.connect(host=self.host, database=self.dbname, user=self.user,
                                            password=self.password, port=self.port)
                self.curs = self.conn.cursor()
                self.isconnected = True
        except psycopg2.DatabaseError as e:
            print(f'Error {e}')

        print(self.conn)

    def insert(self,table_name,headers, data):

            num_iter = list(range(0, math.floor(len(data) / 1000) + 1))

            for i in num_iter:
                print('Inserting ' + str(i + 1) + ' of ' + str(len(num_iter)))
                if i == num_iter[len(num_iter) - 1]:
                    temp_data = data[i * 1000:]
                else:
                    temp_data = data[i * 1000:(i + 1) * 1000]
                idx = 0

                sql_string = 'INSERT INTO ' + table_name + ' (' + ', '.join(headers) + ') VALUES '
                str_values = [None] * len(temp_data)
                idx_local = 0
                if isinstance(data, pd.DataFrame):
                    for index, row in temp_data.iterrows():
                        values_string = ''
                        for elem in row:
                            if type(elem) == str:
                                values_string = values_string + repr(elem) + ","
                            else:
                                values_string = values_string + " " + str(elem) + ","
                        str_values[idx_local] = '(' + values_string[0:len(values_string) - 1] + ')'
                        idx_local += 1
                elif isinstance(data, list):
                    for row in temp_data:
                        values_string = ''
                        for elem in row:
                            if type(elem) == str:
                                values_string = values_string + repr(elem) + ","
                            else:
                                values_string = values_string + " " + str(elem) + ","
                        str_values[idx_local] = '(' + values_string[0:len(values_string) - 1] + ')'
                        idx_local += 1
                sql_string = sql_string + ', '.join(str_values) + ';'
                self.curs.execute(sql_string)
                self.conn.commit()

    def query(self,sql):
        self.curs.execute(sql)
        res_query = self.curs.fetchall()
        columns = self.curs.description

        res = {}
        res_query = list(map(list, zip(*res_query)))

        idx = 0
        for col in enumerate(columns):
            if self.is_empty(res_query,columns):
                res[columns[idx][0]] = {}
            else:
                res[columns[idx][0]] = res_query[idx]
            # res[idx] = my_dict
            idx = idx + 1

        if self.dataframe:
            return pd.DataFrame(res)
        else:
            return res

    def close(self):
        self.curs.close
        self.isconnected = False

    def is_empty(self,mylist,columns):
        if len(columns)>1:
            if len(mylist[0])>0:
                return False
            else:
                return True
        else:
            if len(mylist) > 0:
                return False
            else:
                return True

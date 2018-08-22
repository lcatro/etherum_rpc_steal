
import pymysql

import configure


def query_data(sql_data,debug_output = True) :
    database = pymysql.connect(host = configure.sql_configure['ip'] ,
                               port = configure.sql_configure['port'] ,
                               user = configure.sql_configure['username'] ,
                               password = configure.sql_configure['password'] ,
                               db = configure.sql_configure['database'])
    cursor = database.cursor()

    cursor.execute(sql_data)

    result = cursor.fetchall()
    
    if debug_output :
        print 'query_data:',sql_data
        print 'query_data_result:',result
    
    database.close()
    
    return result

def insert_data(sql_data,debug_output = True) :
    database = pymysql.connect(host = configure.sql_configure['ip'] ,
                               port = configure.sql_configure['port'] ,
                               user = configure.sql_configure['username'] ,
                               password = configure.sql_configure['password'] ,
                               db = configure.sql_configure['database'])
    cursor = database.cursor()

    if debug_output :
        print 'insert_data:',sql_data
        
    cursor.execute(sql_data)
    database.commit()
    database.close()
    

if __name__ == '__main__' :
    print query_data('select * from market')
        
        

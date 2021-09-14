import time


def create_table(columns,table_name):

    sql_string = 'CREATE TABLE IF NOT EXISTS '+table_name+''' (
        ''' #BusinessName VARCHAR(255) UNIQUE, url VARCHAR(255) UNIQUE, PhoneNumber VARCHAR(255), id INTEGER UNIQUE NOT NULL AUTO_INCREMENT, PRIMARY KEY(id)

    for column in columns:
        sql_string += column.name+' '+column.sql_declaration+','

    return sql_string + ' id INTEGER UNIQUE NOT NULL AUTO_INCREMENT, PRIMARY KEY(id));'
#______________________________________________________________________________#

def insert_into(column_dict,table_name):

    sql_string = 'INSERT INTO '+table_name+' ('  #BusinessName,PhoneNumber,url) VALUES (%s,%s,%s)'
    values = list()
    for row in column_dict:
        sql_string += row+','
        values.append(column_dict[row])

    sql_string = sql_string[0:len(sql_string)-1]
    sql_string += ') VALUES ('+'%s,'*len(column_dict.keys())
    sql_string = sql_string[0:len(sql_string)-1]
    #dealing with where statements

    return (sql_string+')' ,tuple(values))

#______________________________________________________________________________#

def update(column_dict,table_name,where):
    sql_string = 'UPDATE '+table_name+' SET '
    values = list()
    for column in column_dict:
        sql_string += column+' = '+'%s, '
        values.append(column_dict[column])

    sql_string = sql_string[0:len(sql_string)-2]
    sql_string +=' WHERE '

    for condition in where:
        sql_string+= condition +' = '+'%s'
        values.append(where[condition])

    return (sql_string,tuple(values))

#______________________________________________________________________________#
print(list(range(2,2,1)))

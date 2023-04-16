import mysql.connector
from mysql.connector import errorcode

class Database():
    def __init__(self):
        self.current_fname = ""
    
    def connect(self):
        try:
            cnx = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password"
            )
            return cnx
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return False
            else:
                return False
    
    def table_exists(self, table_name):
        cnx = self.connect()
        
        if cnx:
            cursor = cnx.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}'")
            return cursor.fetchone()[0] == 1
        
        cursor.close()
        cnx.close()
            
    def create_db(self): # Create
        """Creates database and table"""
        cnx = self.connect()

        if cnx:
            cursor = cnx.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS data_editor")
            cursor.execute("USE data_editor")
            cursor.execute("CREATE TABLE IF NOT EXISTS CSV_Data(filename varchar(255), col_content text(65535), row_content text(65535))")
            
            cursor.close()
        else:
            pass

        cnx.close()   
    
    def save_to_db(self, filename, columns, rows):
        cnx = self.connect()

        if cnx:
            cursor = cnx.cursor()
            cursor.execute("USE data_editor")
            
            query = "INSERT INTO CSV_Data (filename, col_content, row_content) VALUES (%s, %s, %s)"
            values = (filename, columns, rows)
            cursor.execute(query, values)
            cnx.commit()

            cursor.close()
            cnx.close()
        else:
            pass
        
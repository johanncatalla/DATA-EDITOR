import mysql.connector
from mysql.connector import errorcode

class CSVdatabase():
    def __init__(self):
        # Flag to check if a file is opened
        self.current_fname = False
    
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

    def get_fnames(self) -> list:
        """Get 'filenames' from database"""
        cnx = self.connect()

        if cnx:
            cursor = cnx.cursor()
            cursor.execute("USE data_editor")

            # create list of filenames to access specific file
            cursor.execute("SELECT filename FROM CSV_Data")
            results = cursor.fetchall()
            values = [row[0] for row in results]

            if values:
                return values
            
            cursor.close()
            cnx.close()
        else:
            pass

    def get_val_from_fname(self, fname):
        """Get content of filename in database

        Args:
            fname (str): File name from option menu

        Returns:
            str: content of the file
        """
        cnx = self.connect()
        if cnx:
            cursor = cnx.cursor()
            cursor.execute("USE data_editor")

            # select content using filename
            query = "SELECT col_content, row_content FROM CSV_Data WHERE filename = %s"
            self.current_fname = fname

            cursor.execute(query, (fname,))

            result = cursor.fetchall()
            col_row = []
            if result:
                for content in result:
                    for res in content:
                        col_row.append(res)
                return col_row
            
            cursor.close()
            cnx.close()
        else:
            pass
            
    def save_to_db(self, filename, columns, rows):
        """Saves the filename, columns, and rows to database table"""
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
    
    def update_csv(self, fname, columns, rows):
        """Updates the "columns" and "rows" values in the table"""
        cnx = self.connect()
        
        if cnx:
            cursor = cnx.cursor()
            cursor.execute("USE data_editor")
            
            query = "UPDATE CSV_Data SET col_content = %s, row_content = %s WHERE filename = %s"
            values = (columns, rows, fname)

            cursor.execute(query, values)

            cnx.commit()

            cursor.close()
            cnx.close()
        else:
            pass

    def del_from_tbl(self, fname: str): # Delete
        """Delete column using filename"""
        cnx = self.connect()
        if cnx:
            cursor = cnx.cursor()
            cursor.execute("USE data_editor")
            
            query = "DELETE FROM CSV_Data WHERE filename = %s"
            cursor.execute(query, (fname,))

            cnx.commit()

            cursor.close()
            cnx.close()
        else:
            pass
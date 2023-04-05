import mysql.connector

class Database():

    def create_database(self):
        """creates database and table"""
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="yourpassword"
        )

        cursor = cnx.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS text_editor")
        cursor.execute("USE text_editor")
        cursor.execute("CREATE TABLE IF NOT EXISTS Text_Data(filename varchar(255), content text(65535))")
        
        cursor.close()
        cnx.close()

    def save_to_db(self, filename, text):
        """saves the filename and content to database"""
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Catalla109730"
        )

        cursor = cnx.cursor()

        cursor.execute("USE text_editor")
        
        query = "INSERT INTO Text_Data (filename, content) VALUES (%s, %s)"
        values = (filename, text)

        cursor.execute(query, values)

        cnx.commit()

        cursor.close()
        cnx.close()

    def get_fnames(self):
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Catalla109730"
        )
        cursor = cnx.cursor()
        cursor.execute("USE text_editor")

        # create list of filenames to access specific file
        cursor.execute("SELECT filename FROM Text_Data")
        results = cursor.fetchall()
        values = [row[0] for row in results]

        cursor.close()
        cnx.close()

        return values
    
    # TODO open file


if __name__ == "__main__":
    db = Database()
    db.create_database()
    db.save_to_db("test_filename", "test_content")
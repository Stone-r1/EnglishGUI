import mysql.connector
import os
from dotenv import load_dotenv
import sys
import random
import json

load_dotenv()

class Database:
    def __init__(self):
        self.dbHost = os.getenv('DB_HOST')
        self.dbUser = os.getenv('DB_USER')
        self.dbPassword = os.getenv('DB_PASSWORD')
        self.dbName = os.getenv('DB_NAME')
        
        # Connect to the database
        self.mydb = mysql.connector.connect(
            host=self.dbHost,
            user=self.dbUser,
            password=self.dbPassword,
            database=self.dbName,
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
        self.mycursor = self.mydb.cursor()


    def create_table(self):
        wordRecord = """
            CREATE TABLE IF NOT EXISTS WORDS (
            WORD VARCHAR(20) NOT NULL,
            DEFINITION VARCHAR(100) NOT NULL,
            PRIMARY KEY (WORD)
            )
        """
        self.mycursor.execute(wordRecord)


    def check_word_exists(self, word):
        check = """
            SELECT COUNT(*) FROM WORDS WHERE WORD = %s
        """
        self.mycursor.execute(check, (word,))
        return self.mycursor.fetchone()[0]


    def insert_word(self, word, definition):
        insert = """
            INSERT INTO WORDS (WORD, DEFINITION) VALUES (%s, %s)
        """
        self.mycursor.execute(insert, (word, definition))


    def update_word(self, word, definition):
        update = """
            UPDATE WORDS SET DEFINITION = %s WHERE WORD = %s
        """
        self.mycursor.execute(update, (definition, word))

    
    def countWords(self):
        countQuery = """
            SELECT COUNT(*) FROM WORDS
        """
        self.mycursor.execute(countQuery)
        return self.mycursor.fetchone()[0]

    
    def getWords(self, index): 
        self.mycursor.execute("SELECT WORD, DEFINITION FROM WORDS LIMIT 1 OFFSET %s", (index,))
        result = self.mycursor.fetchone()
        return result


    def commit_changes(self):
        self.mydb.commit()


    def close(self):
        self.mydb.close()


if __name__ == "__main__":
    word = sys.argv[1]
    definition = sys.argv[2]
    mode = sys.argv[3]

    db = Database()
    
    if mode == "ADD":
        db.create_table()

        if db.check_word_exists(word) > 0:
            db.update_word(word, definition)
        else:
            db.insert_word(word, definition)

        db.commit_changes()

    elif mode == "START":
        max = db.countWords()
        arr = random.sample(range(0, max), 20)

        wordsDict = {}

        for i in arr:
            result = db.getWords(i)
            if result:
                wordsDict[result[0]] = result[1]

        print(json.dumps(wordsDict))


    db.close()

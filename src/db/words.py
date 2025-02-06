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


    def createTable(self):
        wordRecord = """
            CREATE TABLE IF NOT EXISTS WORDS (
            WORD VARCHAR(20) NOT NULL,
            DEFINITION VARCHAR(100) NOT NULL,
            CATEGORY VARCHAR(50) DEFAULT 'ALL',
            PRIMARY KEY (WORD, CATEGORY)
            )
        """
        self.mycursor.execute(wordRecord)


    def checkWordExists(self, word):
        check = """
            SELECT COUNT(*)
            FROM WORDS
            WHERE WORD = %s
        """
        self.mycursor.execute(check, (word,))
        return self.mycursor.fetchone()[0]


    def insertWord(self, word, definition, category):
        insert = """
            INSERT INTO WORDS (WORD, DEFINITION, CATEGORY)
            VALUES (%s, %s, %s)
        """
        self.mycursor.execute(insert, (word, definition, category))


    def updateWord(self, word, definition, category):
        update = """
            UPDATE WORDS
            SET DEFINITION = %s,CATEGORY = %s 
            WHERE WORD = %s
        """
        self.mycursor.execute(update, (definition, category, word))

    
    def countAllWords(self):
        countQuery = """
            SELECT COUNT(*)
            FROM WORDS
        """
        self.mycursor.execute(countQuery)
        return self.mycursor.fetchone()[0]


    def countCategoryWords(self, category):
        if category == "ALL":
            return self.countAllWords()

        countQuery = """
            SELECT COUNT(*)
            FROM WORDS
            WHERE CATEGORY = %s
        """
        self.mycursor.execute(countQuery, (category,))
        return self.mycursor.fetchone()[0]

    
    def getWordsAll(self, index):
        query = """
            SELECT WORD, DEFINITION
            FROM WORDS
            LIMIT 1 OFFSET %s 
        """
        self.mycursor.execute(query, (index,))
        result = self.mycursor.fetchone()
        return result


    def getWordsCategory(self, index, category):
        if category == "ALL":
            return self.getWordsAll(index)

        query = """
            SELECT WORD, DEFINITION 
            FROM WORDS 
            WHERE CATEGORY = %s 
            LIMIT 1 OFFSET %s
        """
        self.mycursor.execute(query, (category, index))
        result = self.mycursor.fetchone()
        return result


    def commitChanges(self):
        self.mydb.commit()


    def close(self):
        self.mydb.close()


def addWord(db, word, definition, category): 
    db.createTable()

    if db.checkWordExists(word) > 0:
        db.updateWord(word, definition, category)
    else:
        db.insertWord(word, definition, category)

    db.commitChanges()


def startGame(db, category):
    max = db.countCategoryWords(category)

    arr = random.sample(range(0, max), 20)
    wordsDict = {}

    for i in arr:
        result = db.getWordsCategory(i, category)
        if result:
            wordsDict[result[0]] = result[1]

    print(json.dumps(wordsDict))


if __name__ == "__main__":
    word = sys.argv[1]
    definition = sys.argv[2]
    category = sys.argv[3]
    mode = sys.argv[4]

    db = Database()
    
    if mode == "ADD":
        addWord(db, word, definition, category)
    elif mode == "START":
        startGame(db, category)

    db.close()

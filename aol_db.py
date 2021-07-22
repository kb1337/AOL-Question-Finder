import sqlite3


class aol_db:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.connection = sqlite3.connect("aol.db")
        self.cursor = self.connection.cursor()

        q1 = """CREATE TABLE IF NOT EXISTS lectures (
                    lecture_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    lecture TEXT
            )"""

        q2 = """CREATE TABLE IF NOT EXISTS exams (
                    exam_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    lecture_id INTEGER,
                    name TEXT,
                    url TEXT,
                    FOREIGN KEY (lecture_id)
                        REFERENCES lectures (lecture_id)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE     
            )"""

        q3 = """CREATE TABLE IF NOT EXISTS questions (
                    q_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    exam_id INTEGER, 
                    location TEXT,
                    text TEXT, 
                    answer TEXT,
                    FOREIGN KEY (exam_id)
                        REFERENCES exams (exam_id)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE
            )"""

        queries = (q1, q2, q3)
        for q in queries:
            self.cursor.execute(q)
            self.connection.commit()

    def close_connection(self):
        self.connection.close()

    # SELECT
    # -----------------------------------------------------------------
    def show_questions(self):
        q = "SELECT * FROM questions"
        self.cursor.execute(q)
        questions = self.cursor.fetchall()

        if len(questions) == 0:
            print("There isn't any question on database")
        else:
            for question in questions:
                print(question)

    def find_question(self, text):
        query = "SELECT * FROM questions WHERE text LIKE ?"
        self.cursor.execute(query, ("%" + text + "%",))
        questions = self.cursor.fetchall()

        if len(questions) == 0:
            print("Not Found!")
        else:
            print(questions)

    def isConvertedToText(self, img):
        query = "SELECT * FROM questions WHERE location = ? and text = ''"
        self.cursor.execute(query, (img,))
        questions = self.cursor.fetchall()

        if len(questions) == 0:
            return 1
        else:
            return 0

    # INSERT
    # -----------------------------------------------------------------
    def add_lecture(self, lecture):
        query = "INSERT INTO lectures(lecture) VALUES(?)"
        self.cursor.execute(query, (lecture,))
        self.connection.commit()
        return self.cursor.lastrowid

    def add_exam(self, lecture_id, name, url):
        query = "INSERT INTO exams(lecture_id, name, url) VALUES(?, ?, ?)"
        self.cursor.execute(query, (lecture_id, name, url))
        self.connection.commit()
        return self.cursor.lastrowid

    def add_question(self, exam_id, location, text, answer):
        query = (
            "INSERT INTO questions(exam_id, location, text, answer) VALUES(?, ?, ?, ?)"
        )
        self.cursor.execute(query, (exam_id, location, text, answer))
        self.connection.commit()

    # UPDATE
    # -----------------------------------------------------------------
    def update_question(self, location, text):
        query = "SELECT * FROM questions WHERE location = ?"
        self.cursor.execute(query, (location,))
        question = self.cursor.fetchall()

        if len(question) == 0:
            print("Question Not Found")
        else:
            query = "UPDATE questions SET text = ? WHERE location = ?"
            self.cursor.execute(query, (text, location))
            self.connection.commit()
            print("{}\n{}\n{}".format(location, text, "*" * 25))

    # DELETE
    # -----------------------------------------------------------------
    def kitap_sil(self, isim):
        sorgu = "DELETE FROM kitaplar WHERE isim = ?"
        self.cursor.execute(sorgu, (isim,))
        self.connection.commit()

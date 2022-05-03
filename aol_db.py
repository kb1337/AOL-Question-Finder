"""SQLite database for AOL data"""
import sqlite3


class AolDb:
    """Database class for AOL data"""

    def __init__(self):
        self.create_connection()

    def create_connection(self) -> None:
        """Create a database connection to the SQLite database. Create tables if not exists."""
        self.connection = sqlite3.connect("aol.db")
        self.cursor = self.connection.cursor()

        query_1 = """CREATE TABLE IF NOT EXISTS lectures (
                    lecture_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    lecture TEXT
            )"""

        query_2 = """CREATE TABLE IF NOT EXISTS exams (
                    exam_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    lecture_id INTEGER,
                    name TEXT,
                    url TEXT,
                    FOREIGN KEY (lecture_id)
                        REFERENCES lectures (lecture_id)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE     
            )"""

        query_3 = """CREATE TABLE IF NOT EXISTS questions (
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

        queries = (query_1, query_2, query_3)
        for query in queries:
            self.cursor.execute(query)
            self.connection.commit()

    def close_connection(self):
        """Close the database connection"""
        self.connection.close()

    # SELECT
    # -----------------------------------------------------------------
    def show_questions(self) -> None:
        """Show all questions"""
        query = "SELECT * FROM questions"
        self.cursor.execute(query)
        questions = self.cursor.fetchall()

        if len(questions) == 0:
            print("There isn't any question on database")
        else:
            for question in questions:
                print(question)

    def find_question(self, text: str) -> None:
        """Find question by text"""
        query = "SELECT * FROM questions WHERE text LIKE ?"
        self.cursor.execute(query, ("%" + text + "%",))
        questions = self.cursor.fetchall()

        if len(questions) == 0:
            print("Not Found!")
        else:
            print(questions)

    def is_converted_to_text(self, img: str) -> bool:
        """Check if the image is converted to text"""
        query = "SELECT * FROM questions WHERE location = ? and text = ''"
        self.cursor.execute(query, (img,))
        questions = self.cursor.fetchall()

        if len(questions) == 0:
            return 1
        return 0

    # INSERT
    # -----------------------------------------------------------------
    def add_lecture(self, lecture: str) -> int:
        """Add a new lecture to the database"""
        query = "INSERT INTO lectures(lecture) VALUES(?)"
        self.cursor.execute(query, (lecture,))
        self.connection.commit()
        return self.cursor.lastrowid

    def add_exam(self, lecture_id: int, name: str, url: str) -> int:
        """Add a new exam to the database"""
        query = "INSERT INTO exams(lecture_id, name, url) VALUES(?, ?, ?)"
        self.cursor.execute(query, (lecture_id, name, url))
        self.connection.commit()
        return self.cursor.lastrowid

    def add_question(self, exam_id: int, location: str, text: str, answer: str) -> None:
        """Add a new question to the database"""
        query = (
            "INSERT INTO questions(exam_id, location, text, answer) VALUES(?, ?, ?, ?)"
        )
        self.cursor.execute(query, (exam_id, location, text, answer))
        self.connection.commit()

    # UPDATE
    # -----------------------------------------------------------------
    def update_question(self, location: str, text: str) -> None:
        """Update question text"""
        query = "SELECT * FROM questions WHERE location = ?"
        self.cursor.execute(query, (location,))
        question = self.cursor.fetchall()

        if len(question) == 0:
            print("Question Not Found")
        else:
            query = "UPDATE questions SET text = ? WHERE location = ?"
            self.cursor.execute(query, (text, location))
            self.connection.commit()
            print(f"{location}\n{text}")
            print("*" * 25)

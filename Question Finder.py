from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'aol.db')
db = SQLAlchemy(app)

@app.route("/")
def index():
    lectures = Lectures.query.all()
    return render_template("index.html", lectures=lectures)


@app.route("/search", methods=["POST"])
def search():
    text = request.form.get("text")
    lectureID = request.form.get("lectureID")
    search = "%{}%".format(text)

    questionsR = Questions.query.filter(Questions.text.like(search)).all()
    questions = list()

    if lectureID:
        for i in range(0, len(questionsR)):
            if questionsR[i].ex.lecture_id == int(lectureID):
                questions.append(questionsR[i])
    else:
        questions = questionsR

    lectures = Lectures.query.all()
    return render_template("index.html", lectures=lectures, questions=questions)


class Lectures(db.Model):
    lecture_id = db.Column(db.Integer, primary_key=True)
    lecture = db.Column(db.String(80))
    lec = db.relationship("Exams", backref="lec")


class Exams(db.Model):
    exam_id = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey("lectures.lecture_id"))
    name = db.Column(db.String(50))
    url = db.Column(db.String(200))
    ex = db.relationship("Questions", backref="ex")


class Questions(db.Model):
    q_id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.exam_id"))
    location = db.Column(db.String(100))
    text = db.Column(db.String(200))
    answer = db.Column(db.String(3))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

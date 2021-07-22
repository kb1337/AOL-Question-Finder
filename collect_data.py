from bs4 import BeautifulSoup
from aol_db import *
import requests
import wget
import sys
import os


def get_exams(url):
    exams = dict()
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    table_body = table.find("tbody")
    rows = table_body.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        for col in cols:
            a = col.find_all("a")
            if a:
                for link in a:
                    year = cols[0].text.strip("\n").strip("\r")
                    exam_name = link.text[12::].replace(" ", "").strip("\n").strip("\r")

                    exam_name = "{}_{}".format(year, exam_name)
                    exam_url = link.get("href")
                    exams[exam_name] = exam_url
    return exams


def get_exam_details(url):
    Q_A = dict()
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    for question in soup.find_all("div", {"class", "card text-lg-center"}):
        answer = question.get("data-value")

        img = question.find("img", {"class", "QuestionImg"})

        if "soru-bg.gif" in img.get("src"):
            img = img.get("data-src")
        else:
            img = img.get("src")

        print(img)
        wget.download(img)
        print("\n", answer)

        q = img[24::]
        Q_A[q] = answer
    return Q_A

url = ""
lecture_name = ""

if len(sys.argv) != 3:
    sys.stderr.write(
        "Missing Parameters\n\nUsage:\npython %s lacture_name url\n" % sys.argv[0]
    )
    sys.stderr.flush()
    exit()
else:
    lecture_name = sys.argv[1]
    url = sys.argv[2]

base_url = "https://aolsoru.com"

db = aol_db()
lecture_id = db.add_lecture(lecture_name)

directory = "./static"
if not os.path.exists(directory):
    os.makedirs(directory)
os.chdir(directory)

for name, path in get_exams(url).items():
    print("\n{}\n{}\n".format(name, base_url + path))
    exam_id = db.add_exam(lecture_id, name, base_url + path)

    # Inserts questions to database at end of the exam. (every 20 questions in this case.)
    for question, answer in get_exam_details(base_url + path).items():
        db.add_question(exam_id, question, "", answer)
    print("\n\n", "*" * 50)

db.close_connection()
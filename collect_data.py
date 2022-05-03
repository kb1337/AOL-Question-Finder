"""Collects questions and answers from aolsoru.com"""

import sys
import os
import re
from requests import get
from bs4 import BeautifulSoup
from aol_db import AolDb


def download_media(url: str, file_name: str) -> None:
    """Downloads media from url to file_name"""

    print(f"\nDownloading {url} as {file_name}")
    with open(file_name, "wb") as file:
        response = get(url)
        file.write(response.content)
    print(f"Download Successfull. {file_name}")


def get_exams(url: str) -> dict:
    """Returns a dictionary of exam names and urls"""

    exams = {}
    response = get(url, headers={"User-Agent": "Mozilla/5.0"}).content
    soup = BeautifulSoup(response, "html.parser")
    table = soup.find("table")
    table_body = table.find("tbody")
    rows = table_body.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        for col in cols:
            a_tags = col.find_all("a")
            if a_tags:
                for link in a_tags:
                    year = cols[0].text.strip("\n").strip("\r")
                    exam_name = link.text[12::].replace(" ", "").strip("\n").strip("\r")

                    exam_name = f"{year}_{exam_name}"
                    exam_url = link.get("href")
                    exams[exam_name] = exam_url
    return exams


def get_exam_details(url: str) -> dict:
    """Returns a dictionary of questions and answers"""

    questions = {}
    response = get(url, headers={"User-Agent": "Mozilla/5.0"}).content
    soup = BeautifulSoup(response, "html.parser")
    for question in soup.find_all("div", {"class", "card text-lg-center"}):
        answer = question.get("data-value")

        img = question.find("img", {"class", "QuestionImg"})

        if "soru-bg.gif" in img.get("src"):
            img = img.get("data-src")
        else:
            img = img.get("src")

        name = re.search(r"https:\/\/aolsoru\.com\/500\/(.*)", img).group(1)
        download_media(img, name)
        print(answer)

        questions[name] = answer
    return questions


def main() -> None:
    """Main function"""

    url = ""
    lecture_name = ""

    if len(sys.argv) != 3:
        sys.stderr.write(
            f"Missing Parameters\n\nUsage:\npython {sys.argv[0]} lacture_name url\n"
        )
        sys.stderr.flush()
        sys.exit()
    else:
        lecture_name = sys.argv[1]
        url = sys.argv[2]

    base_url = "https://aolsoru.com"

    question_db = AolDb()
    lecture_id = question_db.add_lecture(lecture_name)

    directory = "./static"
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)

    for name, path in get_exams(url).items():
        print(f"\n{name}\n{base_url + path}\n")
        exam_id = question_db.add_exam(lecture_id, name, base_url + path)

        # Inserts questions to database at end of the exam. (every 20 questions in this case.)
        for question, answer in get_exam_details(base_url + path).items():
            question_db.add_question(exam_id, question, "", answer)
        print("\n\n", "*" * 50)

    question_db.close_connection()


if __name__ == "__main__":
    main()

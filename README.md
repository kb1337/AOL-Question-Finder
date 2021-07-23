# AOL Question Finder
Web scraper for [aolsoru.com](https://aolsoru.com/). This website publishes old exam questions publicly. But every question is an image, therefore, you can not search for the specific question. I made the web scraper app that crawls every exam in targetted lecture, downloads images with answers, saves them into SQLite database and converts images to text with OCR. In the end, you can search questions by entering text on the Flask website.

The purpose of the project is for fun.

## Setup 
```sh
pip install -r .\requirements.txt
```

## Usage
**Crawl exams and download questions with answers**
```sh
python collect_data.py <lecture_name> <url>
```
Example:
```sh
python collect_data.py "felsefe1" "https://aolsoru.com/121-kodu-felsefe-1-dersi-sinav-sorulari"
```
**Convert images to string**
```sh
python image_to_string.py
```
**Run flask app**
```sh
python '.\Question Finder.py'
```

## Workflow
Crawl every exam in the lecture url.

<img src="https://user-images.githubusercontent.com/73403802/126779792-b6a7bf38-072e-48da-b0ac-074b211ea946.png" alt="exams" width="500"/>

Every exam has 20 questions.

![questions](https://user-images.githubusercontent.com/73403802/126780648-e3243815-d3b0-47e0-9aae-ea4772395384.png)

Answers are in the `data-value` property.

![answers](https://user-images.githubusercontent.com/73403802/126780502-f2850ce5-009f-4bbe-8836-6c2989255165.png)

## Disclaimer
Sharing questions without permission may cause legal problems.

## License
[MIT](https://github.com/kb1337/AOL-Question-Finder/blob/0419e39cf5cc45cb53ac024fb4c306176a49a34f/LICENSE)

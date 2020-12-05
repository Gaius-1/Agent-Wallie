# Whatsapp News Reporter

<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->
![Python 3.7](https://img.shields.io/badge/Made_With-Python_3.7-green?style=for-the-badge&logo=appveyor)
![GitHub repo size](https://img.shields.io/github/repo-size/squash-bit/Automate-Whatsapp-News)
![GitHub stars](https://img.shields.io/github/stars/squash-bit/Automate-Whatsapp-News?style=social)


With the rapid pace of innovation in the tech industry, it can be difficult for tech professionals, programmers, and Developers to keep their skills current. That being said, reading technology news and blogs every day is one of the best ways to keep up to date on the latest trends and skills needed in tech.

<!--- Add image --->
![Study for Finals](https://github.com/squash-bit/Automate-Whatsapp-News/Assets/Studying-for-finals.jpeg?raw=true)
Finding a few good articles, or blogs to read that are relevant to your area of expertise to follow can sometimes be daunting, not to talk of the time spent scrolling through a plethora of articles that don't interest you.
<!--- Add image --->

![alert](https://github.com/squash-bit/Automate-Whatsapp-News/Assets/bun-alert.png?raw=true)

![Study for Finals](https://github.com/squash-bit/Automate-Whatsapp-News/blob/master/Assests/Studying-for-finals.jpeg?raw=true)

Finding a few good articles, or blogs to read that are relevant to your area of expertise to follow can sometimes be daunting, not to talk of the time spent scrolling through a plethora of articles that don't interest you.
<!--- Add image --->

![alert](https://github.com/squash-bit/Automate-Whatsapp-News/blob/master/Assests/bun-alert.png?raw=true)

I decided to automate the process of searching for current information in the tech industry that might be coming done the road; by scraping a website (eg.Hacker News) for any article I might be interested in, store the title of articles with their links into a database, and finally send them to me on whatsapp.


## Pre-requisites

Before you begin, ensure you have met the following requirements:
<!--- These are just example requirements. Add, duplicate or remove as required --->
* A virtualenv
```python3 -m venv </path/to/new/virtual/environment>```

* You have the version of modules in the requirements.txt file. `requirements.txt` installed in the virtualenv

Or, if not ...

* cd to the directory where requirements.txt is located
* activate your virtualenv

On Windows, run:
```</path/to/virtual/environment>\Scripts\activate.bat```

On Unix or MacOS, run:
```source </path/to/virtual/environment>/bin/activate```

* run: `pip install -r requirements.txt` in your shell


## Description

`news_bot.py` Webscrape and clean markup data from [Hacker News](https://news.ycombinator.com/news) site to get relevant articles. Right after cleaning markup, it sends result to my Whatsapp number using [Twilio sandbox](https://www.twilio.com/).

`main_db.py` Basically creates a connection to SQLite database, creates a Table, insert rows into the Table and store results from `news_bot.py` into Database.

`clock_bot.py` schedules when a function needs to be run

The `logs` folder contains a file named `news_bot.log` which has logs of whatever that happens in the program


## Using Automate Whatsapp News

```
python3 clock_bot.py
```

<!--- Add image showing program runs in session--->
<!-- ![program screenshots](https://github.com/squash-bit/Automate-Whatsapp-News/Assets/screenshots.jpeg?raw=true)-->

You can decide to host the code on [heroku](https://www.heroku.com/)


## Contributors

* [@squash-bit](https://github.com/squash-bit)


## Contact

If you want to contact me you can reach me at
* agbofrederick56@gmail.com
* +233558478823

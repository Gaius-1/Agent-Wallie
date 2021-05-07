# import necessary modules
import os
import re
import requests
import newspaper
from bs4 import BeautifulSoup
from newspaper import Article
from newspaper import Config
from article_summarizer import summarizer
from time import sleep

# clean data
class Cleanser:
    """Scrape the news site and get the relevant updates.."""

    def __init__(self, buzz_words):
        # get the markup from ['https://yourwebpage.com/']
        self.url = 'https://news.ycombinator.com/news'
        self.buzz_words = buzz_words
        self.articles_final = []

    def gather_info(self):
        # get recommended articles[title, link, summary] only for user
        try:
            # scrape only links and titles of articles present in the url:https://news.ycombinator.com/news
            # then summarize each article using it's link...
            r = requests.get(self.url)
            html_soup = BeautifulSoup(r.text, 'html.parser')
            for item in html_soup.find_all('tr', class_='athing'):
                item_a = item.find('a', class_='storylink')
                item_link = item_a.get('href') if item_a else None
                item_text = item_a.get_text(strip=True) if item_a else None

                # list of words that occur most frequent in article
                keywords = self.get_keywords(item_link)
                for buzz_word in self.buzz_words:
                    # find articles that contains any of buzz_words by iterating through the keywords
                    if buzz_word.lower() in keywords:
                        print(keywords)
                        # summarize contents using article_summarizer
                        summary = summarizer(item_link)
                        self.articles_final.append(
                                    {'link'  : item_link,
                                    'title'  : item_text,
                                    'summary': summary})

        except requests.exceptions.SSLError:
            print("Max retries exceeded, Try again later...")

        return self.articles_final

    # get a list of words that occur most frequent in an article
    def get_keywords(self, url):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        config = Config()
        config.browser_user_agent = user_agent
        paper = Article(url, config=config)
        try:
            paper.download()
            paper.parse()
            paper.nlp()
        except:
            return []

        return paper.keywords

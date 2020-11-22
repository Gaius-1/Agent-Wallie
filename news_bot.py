# import necessary modules
import requests
from bs4 import BeautifulSoup
import redis
from twilio.rest import Client
import re

# set up connection
r = redis.Redis(host='localhost', port=6379, db=0)

class Digester:
    """Scrape the news site and get the relevant updates.."""
    def __init__(self, buzz_words):
        # get the markup from ['https://yourwebpage.com/']
        url = 'https://news.ycombinator.com/news'
        self.markup = requests.get(url).text
        self.buzz_words = buzz_words
        self.articles = []

    def parser(self):
        # parse the markup on 'https://news.ycombinator.com/' into an 'html.parser'
        soup = BeautifulSoup(self.markup, "html.parser")
        # find all links in the class attribute 'storylink'
        for item in soup.find_all('tr', class_='athing'):
            # get link
            item_a = item.find('a', class_='storylink')
            item_link = item_a.get('href') if item_a else None
            # get text
            item_text = item_a.get_text(strip=True) if item_a else None
            next_row = item.find_next_sibling('tr')
            # get score
            item_score = next_row.find('span', class_='score')
            item_score = item_score.get_text(strip=True) if item_score else '0 points'
            # We use regex here to find the correct element
            item_comments = next_row.find('a', string=re.compile('\d+(&nbsp;|\s)comment(s?)'))
            item_comments = item_comments.get_text(strip=True).replace('\xa0', ' ') if item_comments else '0 comments'

            self.articles.append({'link': item_link, 'title': item_text, 'score': item_score, 'comments': item_comments})

        self.saved_articles = []

        # find articles that contains any of buzz_words by iterating through the links
        for article in self.articles:
            for buzz_word in self.buzz_words:
                if buzz_word.lower() in article['title'].lower():
                    self.saved_articles.append(article)

    def store(self):
        # store link in the redis database (NoSQL)
        for feed in self.saved_articles:
            r.set(feed['title'], feed['link'])  # the set method of the redis

    def whatsaap(self):
        # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
        # check your twilio dashboard
        account_sid = 'AC3dfa6f36ecf6720af0773fc83d48dc5d'
        auth_token = 'f4430fa7cbf23ca146295ec11c035e8f'
        self.client = Client(account_sid, auth_token)

        # this is the Twilio sandbox testing number
        from_whatsapp_number='whatsapp:+14155238886'
        # replace this number with your own WhatsApp Messaging number
        to_whatsapp_number='whatsapp:+233558478823'
        # try:
        self.client.messages.create(from_=from_whatsapp_number,
                                    body="{} links you might be interested now:\n{}".format(len(self.saved_articles),
                                         "\n\n".join([key.decode("utf-8") + ":  " +r.get(key).decode("utf-8") for key in r.scan_iter()])),
                                    to=to_whatsapp_number)
        print('Message sent successfully...')
        # except:
        #     print('Something went wrong...')

        r.flushdb()  # flush database (redis cache)

# assign this to scheduler to be ran every 6hrs
def recieve_feed():
    # find interested articles
    feed = Digester(['AI', 'ML', 'Machine Learning', 'Artificial Intelligence', 'Data Science', 'Programming', 'Python', 'Matplotlib',
                     'Google', 'Java', 'Linux', 'Software Engineering', 'Data Analytics', 'Numpy', 'Pandas', 'Mathematics'])
    feed.parser()
    feed.store()
    feed.whatsaap()

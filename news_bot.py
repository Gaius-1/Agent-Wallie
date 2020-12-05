# import necessary modules
import requests
import re
import main_db
from main_db import create_connection as connector
from bs4 import BeautifulSoup
from twilio.rest import Client

# Create class to clean data


class Digester:
    """Scrape the news site and get the relevant updates.."""

    def __init__(self, buzz_words):
        # get the markup from ['https://yourwebpage.com/']
        url = 'https://news.ycombinator.com/news'
        self.markup = requests.get(url).text
        self.buzz_words = buzz_words
        self.articles = []

    def scrapper(self):
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
            item_score = item_score.get_text(
                strip=True) if item_score else '0 points'
            # We use regex here to find the correct element
            item_comments = next_row.find(
                'a', string=re.compile('\d+(&nbsp;|\s)comment(s?)'))
            item_comments = item_comments.get_text(strip=True).replace(
                '\xa0', ' ') if item_comments else '0 comments'

            self.articles.append(
                {'link': item_link, 'title': item_text, 'score': item_score, 'comments': item_comments})

        self.saved_articles = []

        # find articles that contains any of buzz_words by iterating through the links
        for article in self.articles:
            for buzz_word in self.buzz_words:
                if buzz_word.lower() in article['title'].lower():
                    self.saved_articles.append(article)

        return self.saved_articles

    def whatsaap(self):
        # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
        # check your twilio dashboard
        account_sid = 'AC3dfa6f36ecf6720af0773fc83d48dc5d'
        auth_token = '309d47f76127c038fe0bf9d2692f39a3'
        self.client = Client(account_sid, auth_token)

        # records holds results from an sql select command
        records = main_db.select_title_and_link(connector(db_file=r"./News_Database.db"))

        # this is the Twilio sandbox testing number
        from_whatsapp_number = 'whatsapp:+14155238886'
        # replace this number with your own WhatsApp Messaging number
        to_whatsapp_number = 'whatsapp:+233558478823'
        try:
            # check if articles are available for me to read.
            if len(records) == 0:
                self.client.messages.create(from_=from_whatsapp_number,
                                            body="There are no articles for you today, Sir.\n\nHappy Coding",
                                            to=to_whatsapp_number)
            # send message
            else:
                self.client.messages.create(from_=from_whatsapp_number,
                                            body="{} Articles you might be interested now:\n{}".format(len(records),
                                                                                                    "\n\n".join([tmp[0] + ":  " + tmp[1] for tmp in records])),
                                            to=to_whatsapp_number)
            print('Message sent successfully...')
        except:
            print('Something went wrong...')

# assign this function to scheduler to be ran every 6hrs
def get_feeds():
    # find interested articles
    feed = Digester(['Machine Learning', 'Artificial Intelligence', 'Data Science', 'Data Analysis'
                     'Python', 'Java', 'Linux',  'Numpy', 'Pandas', 'Mathematics', 'Robotics'])
    articles_and_links = feed.scrapper()
    # yhyh, I don't plan of keeping of the keeping this data ;)
    # I only want updates, not to save for future reference.
    main_db.delete_all_records(connector(db_file=r"./News_Database.db"))
    # store new set of articles
    main_db.store_articles_links(articles_and_links)
    # report them to me through whatsaap
    feed.whatsaap()

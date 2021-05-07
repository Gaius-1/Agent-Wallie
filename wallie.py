# import necessary modules
from telebot import types
from twilio.rest import Client
from jobs import run_continuously
from scraper import Cleanser as agent_wallie
from time import strftime, gmtime
import telebot
import requests
import schedule
import time
import re
import post_news

# bot validation keys
bot_token = '1658967314:AAHp5OgiP0axHOPVR1wHgGmePb9aN2nHsJQ'
bot = telebot.TeleBot(token=bot_token)
chat_id = '1511414464'

# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
# check your twilio dashboard
account_sid = 'AC3dfa6f36ecf6720af0773fc83d48dc5d'
auth_token = 'af318c7d52fafcf2bdf8ba671dea3411'
client = Client(account_sid, auth_token)

# initializations...
global preference, hide_markup
preference = ['Computing', 'Artificial Intelligence', 'Mathematics', 'Physics', 'Machine Learning']
hide_markup = types.ReplyKeyboardRemove()

# welcome user
@bot.message_handler(commands=['start'])
def start_cmd(message):
    # official greetings
    user = message.from_user
    msg =(f"Hello {user.username if user.username else user.first_name}.\nMy name is Walterbot 😊, "
           "my job is to update you on recent findings in these fields by default everyday at 12noon; \n\n"
           "1. Computing & IT \n2. Mathematics \n3. Physics \n4. AI and Machine Learning \n\n"
           "Type '/add' to tailor this list to your preference, or "
           "'/remove' to take out fields you're not interested in... \n"
           "\n\nType '/help' to view all commands \n")

    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['help'])
def aid_cmd(message):
    # list all commands and their use
    help_message =("All bot commands: \n\n"
                   "/add - add to my preference list. \n"
                   "/interests - show all preferences I'm interested in. \n"
                   "/remove - remove an item from my preference list. \n")

    bot.send_message(message.chat.id, help_message)

@bot.message_handler(commands=['add'])
def add_cmd(message):
    # add to list of preferences
    addMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    addMarkup.row('Quantum Computing', 'Artificial Intelligence')
    addMarkup.row('Engineering and Robotics', 'Software Engineering')
    addMarkup.row('Space Exploration', 'Cloud Computing')
    addMarkup.row('Machine Learning', 'Data Science')
    addMarkup.row('Cybersecurity', 'Data Mining')
    addMarkup.row('Physics', 'Google')
    addMarkup.row('Flutter', 'Web Development')
    addMarkup.row('Stocks', 'High Frequency Trading')
    addMarkup.row('Python', 'Competitive Programming')

    sent = bot.send_message(message.chat.id, "Choose what you prefer to add:", reply_markup=addMarkup)
    bot.register_next_step_handler(sent, updater)

def updater(message):
    if message.text in preference:
        bot.send_message(message.chat.id, f"Sorry, '{message.text}' already in your list of preferences. Please choose another.", reply_markup=hide_markup)
    else:
        item = message.text
        preference.append(item)
        bot.send_message(message.chat.id, f"Added '{item}' Successfully...", reply_markup=hide_markup)

# remove an item from a list of added user preferences
@bot.message_handler(commands=['remove'])
def remove_cmd(message):
    addMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    if (len(preference)%2==0):
        for i in range(0, len(preference), 2):
            addMarkup.row(preference[i], preference[i+1])
    else:
        for i in range(0, len(preference), 2):
            if (i==len(preference)-1):
                addMarkup.row(preference[i])
            else:
                addMarkup.row(preference[i], preference[i+1])

    if len(preference) !=0:
        sent = bot.send_message(message.chat.id, "Select what to remove...", reply_markup=addMarkup)
        bot.register_next_step_handler(sent, discard)
    else:
        bot.send_message(message.chat.id, "List is Empty...\n\nType '/add' to update your preference list.")

def discard(message):
    dispose = message.text
    preference.remove(message.text)
    bot.send_message(message.chat.id, f"Removed '{dispose}' successfully", reply_markup=hide_markup)

# display a list of all user's preferences
@bot.message_handler(commands=['interests'])
def display_preference(message):
    msg = ""
    for i in range(1, len(preference)+1):
        msg += f"{i}. {preference[i-1]}\n"

    msg += "\n\nType '/remove' to remove any item you're not interested in."
    bot.send_message(message.chat.id, msg)


if __name__ == '__main__':
    # scrape all necessary information
    def get_all_scraped_info(preference):
        ## curated articles
        my_feed = agent_wallie(preference)
        scraped_info = my_feed.gather_info()
        return scraped_info

    # report news related articles you're interested in at 6pm...
    def report_news():
        print("Loading...")
        scraped_info = get_all_scraped_info(preference)
        # telegram_bot_sendtext(f"I have curated {len(scraped_info)} articles for you today sir!")
        print("Done Gathering..")
        if scraped_info != []:
            for newsletter in scraped_info:
                # use regex to check if it's just a thread of messages on a topic i.e from redit, hackernews, etc
                print("\nChecked. Now In Loop...")
                if re.findall(r'^item\?id=', newsletter['link'], flags=re.MULTILINE) != []:
                    continue
                elif newsletter['summary'] == False or newsletter['summary'] == '':
                    # Customize your message and send update to bot
                    news_update = "{}\n\nClick here to know more: {} ".format(newsletter['title'], newsletter['link'])
                    # update to user through whatsaap
                    post_news.whatsapp(client, "*{}*\n\nClick here to know more: {} ".format(newsletter['title'], newsletter['link']))
                else:
                    # Customize your message and send update to bot
                    news_update = "{}\n\n{}\n\nClick here to know more: {} ".format(newsletter['title'], newsletter['summary'], newsletter['link'])
                    # update user through whatsaap
                    post_news.whatsapp(client, "*{}*\n\n{}\n\nClick here to know more: {} ".format(newsletter['title'], newsletter['summary'], newsletter['link']))

                bot.send_message(chat_id, news_update)
        else:
            # when there's no news update for user...
            bot.send_message(chat_id, "No Latest Updates for Today.\nThank you very much")
            post_news.whatsapp(client, "No Latest Updates for Today.\nThank you very much")

    # Start the background thread
    # update user everyday at 12noon...
    schedule.every().day.at("12:00").do(report_news)
    stop_run_continuously = run_continuously()

    bot.polling(none_stop=True)

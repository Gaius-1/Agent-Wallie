import telebot
from telebot import types
from scraper import Cleanser as agent_wallie
from main_db import StoryDB
from jobs import run_continuously
import requests
import schedule
import time
import re
from time import strftime, gmtime

# bot validation keys
bot_token = '1658967314:AAHp5OgiP0axHOPVR1wHgGmePb9aN2nHsJQ'
bot = telebot.TeleBot(token=bot_token)
chat_id = '1511414464'

# get database file and create a connection
db_file = r"./Assets/News_Database.db"
db_Object = StoryDB(db_file)

# initializations...
global preference, hide_markup, curator
preference = ['Artificial Intelligence']
hide_markup = types.ReplyKeyboardRemove()

# welcome user
@bot.message_handler(commands=['start'])
def start_cmd(message):
    # official greetings
    user = message.from_user
    msg = (f"Hello {user.first_name if user.first_name else ''}.\nMy name is Walter the Reporter, "
           "my job is to update you on recent findings in these fields by default;\n\n1. Computing & IT\n"
           "2. Mathematics\n3. Physics\n4. AI and Machine Learning\n\n"
           "Type '/help' to get assistance on how to use the bot...\n")

    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['help'])
def aid_cmd(message):
    # list all commands and their use
    help_message = ("Hey there, Welcome to the Walter the Reporter Bot's manual. 😊 \n \n"
                   "All bot commands: \n"
                   "💢 /help - Get help message \n"
                   "💢 /add - Update your preference list by adding items\n"
                   "💢 /remove - Feel like removing some items from your preference list? \n"
                   "💢 /store - Want to save some articles for future referencing?\n"
                   "💢 /favourites - See the best articles you've read\n"
                   "💢 /purge - delete all favourites from the database\n"
                   "💢 /description - Short Information about the Bot.\n"
                   "\n\nDeveloped by @squashbit! ")

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
    addMarkup.row('Quants', 'High Frequency Trading')
    addMarkup.row('Hack', 'Mobile Application Development')

    sent = bot.send_message(message.chat.id, "Choose what you prefer to add:", reply_markup=addMarkup)
    bot.register_next_step_handler(sent, updater)

def updater(message):
    if message.text in preference:
        bot.send_message(message.chat.id, f"'{message.text}' already in list, choose another.", reply_markup=hide_markup)
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

# store user's favourite in database
@bot.message_handler(commands=['store'])
def save_cmd(message):
    # get all titles of updates
    current_titles = []
    temporal_keeper = curator
    for news_update in temporal_keeper:
        current_titles.append(new_update['title'])

    # select your favourite
    msg=""
    current_titles = list(enumerate(current_titles))
    for k in current_titles:
        msg += f"{k[0]+1}. {k[1]}"
    sent = bot.send_message(message.chat.id, f"Select a number to save. Space out them if they are many...\n{msg}")
    bot.register_next_step_handler(sent, put_in)

def put_in(message):
    # save it in the database directly...
    pos_list = []
    for i in (message.text).split():
        pos_list.append(curator[int(i)-1])

    StoryDB.save_keep(pos_list)
    bot.send_messaage(message.chat.id, "Submission Successful")

# return user's favourite from the database
@bot.message_handler(commands=['favourites'])
def favourites_cmd(message):
    best = StoryDB.select_title_and_link()
    best = '\n\n'.join(best.split())
    bot.send_message(message.chat.id, f"These are your favourites reads:\n{best}")

# clean database
@bot.message_handler(commands=['purge'])
def purge_cmd(message):
    StoryDB.delete_all_records()
    bot.send_message(message.chat.id, "Clear Successful...")

# Bot's profile
@bot.message_handler(commands=['description'])
def description_cmd(message):
    # give an exhaustive information about the Bot and it's state in development.
    msg = "Bot is currently under construction!!!"
    bot.send_message(message.chat.id, msg)

# apply all settings the bot and report user at 6pm...
# report news related articles you're interested in...
def report():
    print("Loading...")
    ## curated articles
    my_feed = agent_wallie(preference)
    curator = my_feed.gather_info()
    # telegram_bot_sendtext(f"I have curated {len(curator)} articles for you today sir!")
    print("Done Gathering..")
    if curator != []:
        for newsletter in curator:
            # use regex to check if it's just a thread of messages on a topic i.e from redit, hackernews, etc
            print("\nChecked. Now In Loop...")
            if re.findall(r'^item\?id=', newsletter['link'], flags=re.MULTILINE) != []:
                continue
            elif newsletter['summary'] == False or newsletter['summary'] == '':
                ## Customize your message
                my_messages = "{}\n\nClick here to know more: {} ".format(newsletter['title'], newsletter['link'])
            else:
                my_messages = "{}\n\n{}\n\nClick here to know more: {} ".format(newsletter['title'], newsletter['summary'], newsletter['link'])
            # send message to bot
            bot.send_message(chat_id, my_messages)
    else:
        bot.send_message(chat_id, "No Latest Updates for Today.\nThank you very much")

schedule.every().day.at("18:00").do(report)

# Start the background thread
stop_run_continuously = run_continuously()

# # Do some other things...
# time.sleep(10)

# # Stop the background thread
# stop_run_continuously.set()

bot.polling()

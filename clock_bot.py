import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from news_bot import recieve_feed

# append log messages from successive runs to file example.log
logging.basicConfig(filename='./logs/news_bot.log', filemode='w', level=logging.DEBUG)
sched = BlockingScheduler()
# Schedule job_function to be called every six hours
sched.add_job(recieve_feed, 'interval', hours=6)

sched.start()

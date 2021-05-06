# update user on WhatsApp...
def whatsapp(client, news_update):
    # this is the Twilio sandbox testing number
    from_whatsapp_number = 'whatsapp:+14155238886'
    # replace this number with your own WhatsApp Messaging number
    to_whatsapp_number = 'whatsapp:+233558478823'
    try:
        # check if articles are available for me to read.
        # send message
        client.messages.create(from_=from_whatsapp_number, body=news_update, to=to_whatsapp_number)
        print('Message sent successfully...')
    except:
        print('Something went wrong...')

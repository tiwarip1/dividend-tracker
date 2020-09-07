from web_scraper import get_info
import pandas as pd
import smtplib, ssl
import datetime as dt
import time

def is_worktime():
    '''Checks if the current time aligns with regular trading times for the east coast'''
    now = dt.datetime.today()
    if now.date().weekday()<5 and dt.time(16,00) <= now.time() and \
    now.time() <= dt.time(16,30):
        return True
    else:
        return False

def send_email(message):
    '''Sends email'''
    port = 465  # For SSL
    password = 'incrediblysuspiciouspassword'
    
    receiver_email = "shrikanttiwari@yahoo.com"
    sender_email = "incrediblysuspiciousbotemail@gmail.com"
    
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def main():
    
    df = pd.read_csv('tickers.csv')
    counter=0
    
    interesting_tickers = []
    increased_yield = []
    original_yield = []
    
    for i in df['Ticker']:
        print(i)
        counter+=1
        current_yield = round(get_info(i),2)
        try:
            if current_yield>float(df['Yield'].iloc[[counter]].values):
                interesting_tickers.append(i)
                increased_yield.append(current_yield)
                original_yield.append(float(df['Yield'].iloc[[counter]].values))
        except IndexError:
            break
        
    string = ''

    for i in range(0,len(interesting_tickers)):
        string+='{} went from {}% to {}%\n'.format(interesting_tickers[i],original_yield[i],increased_yield[i])

    message = '''Here are a few stocks that have increased their yield value by 20% from their original value:
        
{}'''.format(string)

    send_email(message)

while True:
    if is_worktime():
        main()
    time.sleep(20*60)
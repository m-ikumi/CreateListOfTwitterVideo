#/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
#
# Program name：CreateListOfTwitterVideo.py
#
# Function
#	Search Twitter for a list of videos
#
# Argument
#   (1)Query[Required]:query of 500 characters maximum, including operators.
#   (2)Resulttype:[1]recent  [2]popular  [3]mixed
#                 Default:3
#   (3)Count:Number to be acquired.(Integer value less than 100)
#            Default:15
#   (4)Lang:Target language Ex.) Japanese=ja English=en French=fr …
#           Default:en
#
#/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

#-------------------------------------------------
# Class definition for original error
#-------------------------------------------------
class MyError(Exception):
	# Not_args：Invalid command line argument.
	pass

#-------------------------------------------------
# Function name:sendmail
# Function:Send an email
# Argument:
#   (1)Source email address
#   (2)Destination email address
#   (3)Mail body
#-------------------------------------------------
def sendmail(from_addr, to_addrs, body_txt):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg['From'] = '{} <{}>'.format(Header(gmail_account_nm).encode(), gmail_account)
    msg['To'] = mail_to

    body = MIMEText(body_txt)
    msg.attach(body)

    # Specify the MIME type and file name of the attached file
    attachment = MIMEBase(mine['type'], mine['subtype'], name = attach_file['name'])

    file = open(attach_file['path'], encoding = 'utf-8')
    attachment.set_payload(file.read())
    file.close()
    encoders.encode_base64(attachment)
    msg.attach(attachment)
    attachment.add_header('Content-Dispositon', 'attachment', filename = attach_file['name'])

    # Connect to Gmail
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context = ssl.create_default_context())
    server.login(gmail_account, gmail_password)

    # Send email
    server.sendmail(from_addr, to_addrs, msg.as_string())

#/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
# Main processing
#/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
# gmail account information
gmail_account = '**********@gmail.com'  # Google account (email address)
gmail_password = '**********'           # Google password
gmail_account_nm = '**********'         # Name displayed as source
subject = '**********'                  # Email title to send

# Email destination
mail_to = '**********@*****.com'        # Email destination address

# Setting a Twitter authentication key
consumer_key        = '********************'
consumer_secret     = '********************'
access_token        = '********************'
access_token_secret = '********************'

import os
import sys
import io
import shutil
import glob
import unicodedata
import datetime
import requests
from urllib.error import HTTPError
from urllib.error import URLError

# Loading mail related packages
import smtplib, ssl
from email.header import Header
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Loading twitter related packages
import json
from requests_oauthlib import OAuth1Session

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')

# Command line arguments
args = sys.argv

# Check command line arguments
if not args[1]: # Query
    raise MyError('Not_args')
else:
    q = args[1]
if not args[2]: # Result type
    rt = "mixed"
elif args[2] == "1":
    rt = "recent"
elif args[2] == "2":
    rt = "popular"
else:
    rt = "mixed"
if not args[3]: # Count
    ct = 15
elif int(args[3]) >= 1 and int(args[3]) <= 100:
    ct = int(args[3])
else:
    ct = 15
if not args[4]: # Lang
    lg = "en"
else:
    lg = args[4]

# File save path
path = os.path.join(os.path.abspath(os.path.dirname(__file__)))

# Creating common mail data (MIME)
mine = {'type':'application', 'subtype':'json'}
attach_file = {'name': 'original.json', 'path': path + '/original.json'}

# TwetterOAuth authentication
twitter = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)

# search / tweets API
url_search = 'https://api.twitter.com/1.1/search/tweets.json'

# Search parameters
params = {'q': q, 'result_type': rt, 'count': ct, 'lang': lg}

try:
    # search/tweet API execution
    res = twitter.get(url_search, params = params)

    # Check response
    if res.status_code == 200: # normal
        # Read execution result (json)
        tweet = json.loads(res.text)

        # Get current date and time
        dt_now = datetime.datetime.now()

        # json dump output
        with open(path + '/original.json', mode='w', encoding='utf-8') as f:
            json.dump(tweet, f, ensure_ascii=False, indent=4, separators=(',', ': '))
        # List file output
        with open(path + '/list.lst', mode='w', encoding='utf-8') as f:

            f.write('Checked on ' + dt_now.strftime('%Y/%m/%d %H:%M:%S') + '\n')
            f.write('Query:' +  params['q'] + '\n')
            f.write('result type:' +  params['result_type'] + '\n')
            f.write('count:' +  str(params['count']) + '\n')
            f.write('lang:' +  params['lang'] + '\n')

            # Loop by tweet
            for post in tweet['statuses']:
                i_cnt = 0

                # Loop by entity
                for ent in post['entities']:
                    if 'media' in ent: # Process only if there is media
                        url = ''
                        # Loop by media
                        for media in post['extended_entities']['media']:
                            # There is a url and only for videos
                            if media['expanded_url'] != '' and media['type'] == 'video':
                                # Write various information
                                f.write('*************************************************\n')
                                f.write('User name：' + post['user']['name'] + '\n')
                                f.write('Tweet：' + post['text'] + '\n')
                                f.write('Posted date' + post['created_at'] + '\n')
                                f.write('Favorites' + '{:,}'.format(post['favorite_count']) + '\n')
                                f.write('Video URL：' + media['expanded_url'] + '\n')
                                break
        file = open(path + '/list.lst', mode='r', encoding='utf-8')
        mail_body = file.read()
        file.close()

        # send e-mail
        sendmail(gmail_account, mail_to, mail_body)

except MyError as e:
    tb = sys.exc_info()[2]
    if str(e.with_traceback(tb)) == 'Not_args':
        mail_body = '********** Error occurred **********\n<<Invalid command line argument.>>'
        sendmail(gmail_account, mail_to, mail_body)

except Exception as e:
    import traceback
    mail_body = '********** Error occurred **********\n<<An unknown error has occurred.>>\n'
    mail_body += traceback.print_exc()
    sendmail(gmail_account, mail_to, mail_body)

# -*- coding: utf-8 -*-
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_schedule():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    now = datetime.datetime.now()    
    #print(now)
    today_start = str(now.year) + '-' + str(now.month).zfill(2) + '-' + str(now.day).zfill(2) + 'T00:00:00+09:00'
    today_end = str(now.year) + '-' + str(now.month).zfill(2) + '-' + str(now.day).zfill(2) + 'T23:59:59+09:00'
    
    weekday = datetime.date.today().weekday() #曜日の取得
    weekday_list = ["月","火","水","木","金","土","日"]


    eventsResult = service.events().list(
        calendarId='primary', timeMin=today_start, timeMax=today_end, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    event_text = '。おはようございます。十時です。本日は、' + str(now.year) + '年、' + str(now.month) + '月、' + str(now.day) + '日、' + str(weekday_list[weekday]) + '曜日、です。今日の、研究室行事は、'
    
    if not events:
        event_text += 'ありません。'
	
	if weekday == 0:
	    event_text += '今週も一週間、がんばりましょう！'
        print(event_text)
        return event_text

    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
	    event_text += str(start[11:13])+'時'+str(start[14:16])+'分、から、'
            event_text += event['summary'].encode('utf_8')
	    if event == events[-1]:
		event_text += '。です。'
	    else:
		event_text += '。と、'
	
	if weekday == 0:
	    event_text += '今週も一週間、がんばりましょう！'
        print(event_text)
        return event_text

if __name__ == '__main__':
    get_schedule()

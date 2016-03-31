import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import datetime
import re

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Quickstart'


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
                                   'calendar-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print ('Storing credentials to ' + credential_path)
    return credentials

def main():
    info = ''
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print ('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='6mpjb4upohrsbp57oo0qe0ctak@group.calendar.google.com', timeMin=now, maxResults=12, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print ('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print (start, event['summary'])
        info += start + '  ' + event['summary'] + '\n'
    print(info)
    img = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 16)
    draw.text((0,0), info, font=font, fill='#8888ff')
    img.save('WPIClasses.jpg')

    info = ''
    eventsResult = service.events().list(
        calendarId='binamenator@gmail.com', timeMin=now, maxResults=24, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print ('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print (start, event['summary'])
        info += start + '  ' + event['summary'] + '\n'
        tempstr = re.compile('[0-9][0-9]\:')
        tempstr = tempstr.match(start + '  ' + event['summary'] + '\n')
        print('This is tempstr:')
        print(tempstr)
    print(info)
    
    img = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 16)
    draw.text((0,0), info, font=font, fill='#8888ff')
    img.save('events.jpg')



if __name__ == '__main__':
    main()

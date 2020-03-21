from __future__ import print_function
from django.utils.encoding import smart_str, smart_unicode
import pickle
import os.path, re, sys, getpass
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    curUser = getpass.getuser()
    REPORT_MSG = "Hello " + curUser + "! "

    # Call the Gmail API to get the list of unread emails received in last 24 hours
    response = service.users().messages().list(userId='me', q="is:unread newer_than:1d").execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId='me', q="is:unread newer_than:1d",
                                          pageToken=page_token).execute()
      messages.extend(response['messages'])

    mailCount = response['resultSizeEstimate']
    if mailCount > 0:
      SENDER_LIST = []
      REPORT_MSG = REPORT_MSG + "You have received " + str(mailCount) + " new emails in last 24 hours! Here is the sender list: "

    else:
      REPORT_MSG = REPORT_MSG + "You have no new emails to read! That's all for now. Thank you for using the service!"
      sys.stdout = open('emailReport.txt', 'w')
      print(smart_str(REPORT_MSG))
      quit()


    # Call the Gmail API to get metadata of all the emails
    for i in range(mailCount):
      messageId = str(response['messages'][i]['id'])
      message = service.users().messages().get(userId='me', id=messageId).execute()
      header = message['payload']['headers']
      senderIndex = header.index(filter(lambda n: n.get('name') == 'From', header)[0])
      senderAddress = header[senderIndex]['value']
      a = re.sub('<[^>]+>', '', senderAddress)
      sender = (a.strip()).replace("\"", "")
      SENDER_LIST.append(sender)

    j = set(SENDER_LIST)
    uniqueSender = list(j)

    for z in range(len(uniqueSender)):
      count = SENDER_LIST.count(uniqueSender[z])
      REPORT_MSG = REPORT_MSG + str(count) + " mail from " + SENDER_LIST[z] + ". "

    REPORT_MSG = REPORT_MSG + "That's all for now. Thank you for using the service! "
    sys.stdout = open('emailReport.txt', 'w')
    print(smart_str(REPORT_MSG))

if __name__ == '__main__':
    main()

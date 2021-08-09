from __future__ import print_function
import nltk
import nltk
from nltk.corpus import movie_reviews
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
from nltk.sentiment import SentimentIntensityAnalyzer


sia = SentimentIntensityAnalyzer()

no_of_emails = 5


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
creds = None

if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('gmail', 'v1', credentials=creds)
    
results = service.users().messages().list(userId='me').execute()

labels = results.get('messages', [])

if not labels:
    print('No labels found.')
else:
    #print('Labels:')
    i = 1
    for label in labels:
        
        re = service.users().messages().get(userId='me',id=label['id']).execute()        
    
        
        if re['payload'].get('parts') is not None:
            try:
                data = (re['payload'].get('parts')[0]['body']['data'])
                
                data = data.replace("-","+").replace("_","/")
                
                decoded_data = base64.b64decode(data)
                #print(decoded_data)                
                
                d = decoded_data.decode('UTF-8')
                #print(d)
                
                scores = sia.polarity_scores(d)
                print(scores)
                if scores['compound'] >= 0.05:
                    print("email is positive")
                elif scores['compound'] <= -0.05:
                    print("email is negative")
                else:
                    print("email is neutral")
                #print("---------------------------------------------")
                    
            except KeyError:
                pass
                #print("keyerror")
                #print("---------------------------------------------")
            
        if i>=no_of_emails:
            break
        i+=1
        
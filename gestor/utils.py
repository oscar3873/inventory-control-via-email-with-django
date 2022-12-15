import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Si se modifica el scope , hay que eliminar el token.json

SCOPES = ['https://www.googleapis.com/auth/calendar']

creds = None

def googleCalendarConection():
    """Rutina para poder conectarnos a la API de google Calendar
    """
    global creds
    # El archivo token.json almacena los tokens de acceso y actualización del usuario, y es
    # creado automáticamente cuando el flujo de autorización se completa por primera vez
    # tiempo.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Si no hay credenciales (válidas) disponibles, permita que el usuario inicie sesión.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Guarde las credenciales para la próxima ejecución
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

def insertGoogleCalendar(evento):
    global creds
    googleCalendarConection()
    
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Post event')
        
        event = service.events().quickAdd(
            calendarId='cb3a126e4645f8d1de693dc10177e7d3a3d684e0edfd5e4622ba7e722c0b53f2@group.calendar.google.com',
            text=evento
        ).execute()
        
        if not event:
            print('No upcoming events found.')
            return    
        print('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)
          

def getEventsGoogleCalendar():
    
    googleCalendarConection()

    ######### Getting ##########
    
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(
            calendarId='cb3a126e4645f8d1de693dc10177e7d3a3d684e0edfd5e4622ba7e722c0b53f2@group.calendar.google.com'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)
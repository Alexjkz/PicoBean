import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


filesDir = os.path.dirname(os.path.abspath(__file__))

# path of file json
credentials_file = os.path.join(filesDir, "credentials.json")
token_file = os.path.join(filesDir, "token.json")


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def authorization():
  '''
  Verifica che ci sia il token legato alle credenziali dell'utente. 
  Se manca, chiede il login per creare il token.json
  '''
  
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(token_file):
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          credentials_file, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_file, "w") as token:
      token.write(creds.to_json())
  # ritorna le credenziali
  return creds
  



def getTodaySchedules(creds, shiftStart, shiftEnd):
  '''
  Restituisce una lista di dizionari contenente l'orario (key) associato ad un evento (value)
  
  creds sono le credenziali dell'utente -> vedi authorization()
  shiftStart -> intero che serve per determinare il giorno di inizio di ricerca delle attività -> con 0 cerca nel giorno corrente, 
                                                                                                  con 1 aggiunge un giorno alla data odierna -> cerca le attività di domani
  shiftEnd -> limite di ricerca delle attività -> con 1 cerca fino a fine giornata odierna
                                               -> con 2 cerca fino alla fine del giorno dopo

  '''  

  # Elenco degli eventi della giornata
  dailyEvents = []  
  try:
    service = build("calendar", "v3", credentials = creds)

    # Call the Calendar API
    now = (datetime.datetime.utcnow() + datetime.timedelta(days=shiftStart)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"    # 'Z' indicates UTC time
    end_of_day = (datetime.datetime.utcnow() + datetime.timedelta(days=shiftEnd)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"    
   
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            timeMax = end_of_day,           
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )   
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:   
      # print(event)
      start = datetime.datetime.fromisoformat(event["start"].get("dateTime", event["start"].get("date")))      
      summary = event['summary']
      dailyEvent = {start.strftime("%H:%M") : summary}
      dailyEvents.append(dailyEvent)    
    
    return dailyEvents
  
    
 

  except HttpError as error:
    print(f"An error occurred: {error}")


def getActivities(giornoRichiesto):
  '''
  Restituisce la lista di stringhe con l'orario e l'evento a seconda del giorno richiesto (Solo oggi o domani)
  '''
  activitiesTTS = [] # lista di stringhe da dare in pasto al tts  
  creds = authorization() # prendo i creds 
  dailyEvents = getTodaySchedules(creds, shiftStart=0 if giornoRichiesto == "Impegni_Oggi" else 1, shiftEnd=1 if giornoRichiesto =="Impegni_Oggi" else 2)     
  if (dailyEvents == None):
    return None
  else :
    print("I tuoi impegni di oggi sono : ")
    print(dailyEvents)
    for event in dailyEvents :    
      ora = list(event.keys())[0]
      objToRead = f"ore {ora.replace(':' , ' e ')}, {event[ora]}"
      activitiesTTS.append(objToRead)
    
  return activitiesTTS






# def main():  
#   creds = authorization() # prendo i creds 
#   dailyEvents = getTodaySchedules(creds)

#   print("I tuoi impegni di oggi sono : ")
#   for event in dailyEvents :    
#     ora = list(event.keys())[0]
#     objToRead = f"ore {ora.replace(':' , ' e ')}, {event[ora]}"
#     print(objToRead)
  

# if __name__ == "__main__":
#   main()


import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

# This function looks for the .env file and loads the variables
load_dotenv()

# Now you can safely access them
sid = os.getenv('TWILIO_ACCOUNT_SID')
token = os.getenv('TWILIO_AUTH_TOKEN')

TWILIO_PHONE_NUMBER='+16293171352'




# 2. Meteoblue API
METEOBLUE_URL = "https://my.meteoblue.com/packages/basic-1h_basic-day?apikey=Pv1z2bAu3t5RE0i8&lat=30.0626&lon=31.2497&asl=23&format=json"
response = requests.get(METEOBLUE_URL).json()

times = response['data_1h']['time']
precip = response['data_1h']['precipitation']

# 3. Logic to check for rain in the next 12 hours
rain_found = False
for i in range(12):
    if precip[i] > 0:
        print(f"Rain predicted at {times[i]}: {precip[i]} mm")
        rain_found = True

# 4. Send only ONE alert if rain is found at any point in the 12 hours
if rain_found:
    client = Client(sid , token)
    message = client.messages\
    .create(
        body="Rain is expected in Cairo within the next 12 hours. Prepare accordingly!",
        from_=TWILIO_PHONE_NUMBER,
        to="01006100111"
    )
    print(message.status)
else:
    print("No rain predicted for the next 12 hours.")

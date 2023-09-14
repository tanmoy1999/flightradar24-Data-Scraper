import requests
import pandas as pd
import datetime

def epoch(ts):
  timestamp = datetime.datetime.fromtimestamp(ts)
  formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
  return formatted_timestamp


flight_id = '31ded076'
# Define the API endpoint URL
url = 'https://data-live.flightradar24.com/clickhandler/?version=1.5&flight=' + flight_id  # Replace with the actual API endpoint URL
# https://www.flightradar24.com/flights/most-tracked


# Send a GET request to the API
response = requests.get(url)

df_trails = pd.DataFrame(columns=["flight_id", "trail_lat", "trail_lng", "trail_alt", "trail_spd", "trail_ts", "trail_hd"])
df_aircraft = pd.DataFrame(columns=["flight_id","model_code", "model_aircraftType", "model_countryID", "model_registration"])

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    print(len(data['trail']))
    # Now 'data' contains the JSON data returned by the API

    # Trails
    for i in range(len(data['trail'])):
      lat = data['trail'][i]['lat']
      lng = data['trail'][i]['lng']
      alt = data['trail'][i]['alt']
      spd = data['trail'][i]['spd']
      ts = epoch(data['trail'][i]['ts'])
      hd = data['trail'][i]['hd']
      df1 = pd.DataFrame(data=[[flight_id,lat,lng,alt,spd,ts,hd]],columns=["flight_id", "trail_lat", "trail_lng", "trail_alt", "trail_spd", "trail_ts", "trail_hd"])
      df_trails = pd.concat([df_trails,df1], axis=0)

    # Aircraft
    model_code = data['aircraft']['model']['code']
    model_aircraftType = data['aircraft']['model']['text']
    model_countryID = data['aircraft']['countryId']
    model_registration = data['aircraft']['registration']
    df2 = pd.DataFrame(data=[[flight_id,model_code,model_aircraftType,model_countryID,model_registration]],columns=["flight_id","model_code", "model_aircraftType", "model_countryID", "model_registration"])
    df_aircraft = pd.concat([df_aircraft,df2], axis=0)
    print(flight_id,model_code,model_aircraftType,model_countryID,model_registration)

    
else:
  print(f"Failed to retrieve data. Status code: {response.status_code}")

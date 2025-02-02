from dotenv import load_dotenv
import os
from classes.building_consent import BuildingConsent
from openai import OpenAI
import requests


#region KEYS #################################
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), './setup/.env'))

# Set API keys
# OpenAI.api_key = os.getenv("OPEN_AI_KEY")
visual_weather_key = os.getenv("VISUAL_CROSSING_KEY")
open_route_key = os.getenv("OPEN_ROUTE_KEY")

db_params = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
}

bc_number = 1 #example bc number
#fetch building consent from database, returning a tuple of (bc_number, level, location)
consent = BuildingConsent.fetch_from_db(bc_number, db_params)

#endregion ###################################

#region  OPENAPI METHODS #####################
context =  """*Context**: you are an AI model for scheduling council building inspections (Datacom).
            If the user asks about something irrelevant, consider providing an answer but remind them you're focused on helping them for booking inspections.
            Response: Always format your response as if it will be used as inner.html, without backquotes etc."""

def getResponse(message, context=context):
    """
    Generates a response from OpenAI's GPT model.
    """
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Specify the model name
        messages=[
            {"role": "system", "content": context}, 
            {"role": "user", "content": message}
            ], 
        max_tokens=700,  # Limit the response to a maximum of 700 tokens
        temperature=0.3,  # Set the temperature for randomness in generation
        frequency_penalty=0,  # Control the penalty for repeated tokens
        presence_penalty=0  # Control the penalty for new topic introduction
    )
    # Return the content of the first choice from the response
    return completion.choices[0].message

def getBoolResponse(message):
    """
    Returns a boolean response from the model based on the message.
    """
    result = getResponse(message, "ONLY reply with 'yes' or 'no.'")
    return result.lower() == "yes" #return true if yes, else false


# def getHTMLResponse(message, context):
#     """
#     Generates an HTML response from OpenAI's GPT model.
#     """
#     # Add the context to the input message
#     return getResponse(context,message)

#endregion  ##################################

#region Weather - Visual Crossing API ########
def fetch_visual_weather_data(location="Morrinsville", date="2024-09-23", time="13:00:00"):
    """
    Fetches the forecast string, eg 'Cloudy, Overcast' at the given values
    """
    # Construct the URL for the API request
    w_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location},%NZ/{date}T{time}?key={visual_weather_key}"
    print("w_url: " + w_url)
    # Make the API request and parse JSON response
    response = requests.get(w_url)
    response = response.json()
    # Iterate through the hours of the day
    hours = response['days'][0]['hours']
    for hour in hours:
        # Check if the current hour matches the given time
        if hour['datetime'] == time:
            return hour['conditions']
    # Return None if the forecast string is not found
    return None

#endregion  #################################

#region Distance - Open Route Service API ########
def fetch_open_distance_data(start="Morrinsville", end="180 Knighton Road"):
    """
    Fetches the travel distance in kilometers and duration from the Open Route Service API.
    """

    start_coords = fetch_coordinates(start)
    end_coords = fetch_coordinates(end)

    url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={open_route_key}&start={start_coords[0]},{start_coords[1]}&end={end_coords[0]},{end_coords[1]}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        segment = data["features"][0]["properties"]["segments"][0]
        distance = int(segment["distance"]) / 1000  # Distance in meters
        duration = segment["duration"]  # Duration in seconds

        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)

        return {
            "distance": f"{distance:.2f} kms",
            "duration": f"{hours} hours, {minutes} minutes"
        }

    print(f"Request failed with status code: {response.status_code}")
    return {}

def fetch_coordinates(address="Waikato University, Hamilton"):
    """
    Get coordinates of an address.
    """

    api_address = "%20".join(address.split()).replace(',', '')
    url = f'https://api.openrouteservice.org/geocode/search?api_key={open_route_key}&text={api_address}&boundary.country=NZL&size=1'

    response = requests.get(url).json()

    if response['features']:
        coordinates = response['features'][0]['geometry']['coordinates']
        return coordinates

    print("No coordinates found.")
    return []

#endregion  #################################




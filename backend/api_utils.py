from dotenv import load_dotenv


#region KEYS #################################-
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../setup/.env'))

api_key = os.getenv("OPEN_AI_KEY")
openai.api_key = api_key
visual_weather_key = os.getenv("VISUAL_CROSSING_KEY")
open_route_key = os.getenv("OPEN_ROUTE_KEY")

#static file path to grab building consent json
file_path = os.path.join(os.getcwd(), 'data/consents/consent_1.json')
#Init building consent class to grab inspection type
CONSENT = BuildingConsent(file_path)
inspection_type = CONSENT.type

# Verification
if api_key:
    print("OpenAI key loaded successfully!")
else:
    print("Failed to load OpenAI key.")

#endregion ###################################
import os
from dotenv import load_dotenv
from datetime import datetime
from classes.building_consent import BuildingConsent
from classes.inspection import Inspection
import inspection_scheduling


#temporarily being used to test backend functions 

#load db_params
load_dotenv(dotenv_path='setup/.env')
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

def main():
    #user input for testing
    inspection_date = input("Enter inspection date (YYYY-MM-DD): ")
    bc_number = 1
    try:
        inspection_date = datetime.strptime(inspection_date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please enter a date in the format YYYY-MM-DD.")
        return
 
    #init building consent instance
    building_consent = BuildingConsent.fetch_from_db(bc_number, db_params)

    #check weather based on date
    if inspection_scheduling.not_valid_weather(inspection_date, building_consent.location):
        print("Weather is not suitable for inspection. Please choose another Date")
        return

    #get qualified inspectors based on building consent level
    qualified_inspectors = inspection_scheduling.get_qualified_inspectors(db_params, building_consent.level)
    print(qualified_inspectors)
 


    
    
if __name__ == '__main__':
    main()
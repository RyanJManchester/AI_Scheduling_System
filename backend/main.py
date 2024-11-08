import os
from dotenv import load_dotenv
from datetime import datetime
from classes.building_consent import BuildingConsent
from classes.inspection import Inspection
from classes.inspector import Inspector
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
    bc_number = 1
    inspection_date = "2024-10-01"
    working_hours = {'start': '09:00', 'end': '17:00'}
 
    #init building consent instance
    building_consent = BuildingConsent.fetch_from_db(bc_number, db_params)
    print(building_consent)

    #step 1: Check weather for location
    # weather is working

    #step 2: Get qualified inspectors based on building consent level
    qualified_inspectors = inspection_scheduling.get_qualified_inspectors(db_params, building_consent.level)
    print(qualified_inspectors)

    #step 3: Get available schedules for qualified inspectors
    available_schedules = inspection_scheduling.get_available_schedules(working_hours,qualified_inspectors, inspection_date, db_params) 

    # #step 4: Calculate distance from last known location to inspection site
    # distance_info_list = []
    # for inspector_id, available_slots in available_schedules.items():
    #     inspector_availability = {inspector_id: available_slots}

    #     inspector_distances = inspection_scheduling.get_distances(inspector_availability, building_consent.location)
    #     distance_info_list.append(inspector_distances)
    # print("distance information for inspectors: ")
    # for info in distance_info_list:
    #     print(info)

    distance_info_list_test = [
        [{'inspector_id': 8, 'distance': '0.00 kms', 'duration': '0 hours, 0 minutes', 'last_known_location': '1 Smith Street, Hamilton', 'inspection_location': '1 Smith Street, Hamilton'}],
        [{'inspector_id': 9, 'distance': '2.85 kms', 'duration': '0 hours, 5 minutes', 'last_known_location': 'Municipal Offices, Garden Place, Hamilton, New Zealand', 'inspection_location': '1 Smith Street, Hamilton'}],
        [{'inspector_id': 10, 'distance': '2.85 kms', 'duration': '0 hours, 5 minutes', 'last_known_location': 'Municipal Offices, Garden Place, Hamilton, New Zealand', 'inspection_location': '1 Smith Street, Hamilton'}],
        [{'inspector_id': 11, 'distance': '2.85 kms', 'duration': '0 hours, 5 minutes', 'last_known_location': 'Municipal Offices, Garden Place, Hamilton, New Zealand', 'inspection_location': '1 Smith Street, Hamilton'}],
        [{'inspector_id': 12, 'distance': '2.85 kms', 'duration': '0 hours, 5 minutes', 'last_known_location': 'Municipal Offices, Garden Place, Hamilton, New Zealand', 'inspection_location': '1 Smith Street, Hamilton'}]
        ]

    #step 5: Produce a list of suggested slots based on closest distance to last known location
    suggestions = inspection_scheduling.get_suggestions(distance_info_list_test, available_schedules)
    print("suggestions: ")
    print(suggestions)
    
    
    
if __name__ == '__main__':
    print('starting...')
    main()
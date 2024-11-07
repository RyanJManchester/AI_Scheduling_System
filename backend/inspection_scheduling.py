import api_utils
import psycopg2
from classes.inspector import Inspector
from datetime import datetime, timedelta

###Scheduling logic ###
# Check if weather is suitable for inspcetion
# Get qualified inspectors
# Check their respective schedules, and have available if more than 2 hours
# For each of their available slots, get distance from last known location
# Produce a list of best slots based on closest distance to last known location

def not_valid_weather(inspection_date, inspection_location):
    """
    Checks if the weather conditions are not suitable for inspection.
    """
    inspection_location = inspection_location.replace(" ", "%20")

    # Fetch the weather condition
    weather_condition = api_utils.fetch_visual_weather_data(location=inspection_location, date=inspection_date)
    print(weather_condition)

    # Check if the weather condition contains 'rain' or 'snow'
    if weather_condition and ("rain" in weather_condition.lower() or "snow" in weather_condition.lower()):
        return True
    return False

def get_qualified_inspectors(db_params, inspection_type):
    """
    This function filters for qualified inspectors based on inspection type.
    """
    qualification_hierarchy = {
        "R1": ["R1", "R2", "R3", "R4"],
        "R2": ["R2", "R3", "R4"],
        "R3": ["R3", "R4"],
        "R4": ["R4"],
        "C1": ["C1", "C2", "C3", "C4"],
        "C2": ["C2", "C3", "C4"],
        "C3": ["C3", "C4"],
        "C4": ["C4"]
    }
    # Fetch valid qualifications based on inspection type
    valid_qualifications = qualification_hierarchy.get(inspection_type, [])
    print("Valid qualifications:", valid_qualifications)

    qualified_inspector_ids = []
    # Connect to the database and fetch all inspectors
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # SQL query to fetch all inspectors
    cursor.execute("SELECT id FROM Inspector")
    #fetchall() returns a list of tuples, so we need to convert it
    inspectors_ids_tuple = cursor.fetchall()
    inspectors_ids = [inspector[0] for inspector in inspectors_ids_tuple]

    qualified_inspector_ids = []
    #iterate through inspectors in inspectors_data
    for inspector_id in inspectors_ids:
        inspector = Inspector.fetch_from_db(inspector_id, db_params)
        # Determine which qualification list to check based on inspection type
        if inspection_type.startswith('R'):
            # Check residential qualifications
            qualifications_to_check = inspector.residential_qual
        else:
            # Check commercial qualifications
            qualifications_to_check = inspector.commercial_qual

        if qualifications_to_check in valid_qualifications:
            qualified_inspector_ids.append(inspector.id)

    print("Qualified inspectors:")
    print(qualified_inspector_ids)
    return qualified_inspector_ids

def calculate_available_slots(schedule, working_hours):
    """
    Calculates the available time slots for inspectors based on their schedules, designated working hours and tracks thier last known location
    """
    available_slots = []
    start_of_day = datetime.strptime(working_hours['start'], '%H:%M')
    end_of_day = datetime.strptime(working_hours['end'], '%H:%M')

    #start with the start of the day and no known last location
    current_start = start_of_day
    last_known_location = "Municipal Offices, Garden Place, Hamilton, New Zealand"
    for inspection in schedule:
        inspection_start = datetime.strptime(inspection['inspection_start_time'], '%H:%M')
        inspection_end = datetime.strptime(inspection['inspection_end_time'], '%H:%M')

        #check if there is a gap before the current inspection
        if inspection_start > current_start:
            available_duration = inspection_start - current_start
            #only return timeslots longer than 2 hours
            if available_duration >= timedelta(hours=2):
                available_slots.append({
                    "start": current_start.time(),
                    "end": inspection_start.time(),
                    "last_known_location": last_known_location
                })
        
        #update last known location
        last_known_location = inspection['inspection_location']
        #move current_start time to the end of this inspection
        current_start = inspection_end
    
    #check for a slot between the last inspection and the end of the work
    if current_start < end_of_day:
        available_duration = end_of_day - current_start
        if available_duration >= timedelta(hours=2):
            available_slots.append({
                "start": current_start.time(),
                "end": end_of_day.time(),
                "last_known_location": last_known_location
            })

    return available_slots

    
def get_available_schedules(working_hours, inspector_ids, inspection_date, db_params):
    """
    Gets the available time slots for inspectors based on their schedules from the database. 
    It only returns timeslots that longer than 2 hours.
    """
    filtered_slots = {}

    for inspector_id in inspector_ids:
        #fetch inspector's schedule for the given date
        schedule = Inspector.get_schedule_for_date(inspector_id, inspection_date, db_params)
        print("schedule: ")
        print(schedule)

        #calculate available slots
        if schedule:
            available_slots = calculate_available_slots(schedule, working_hours)
        else:
            #no inspections scheduled, so whole day is available
            available_slots = [{
                "start": datetime.strptime(working_hours['start'], '%H:%M').time(),
                "end": datetime.strptime(working_hours['end'], '%H:%M').time(),
                "last_known_location": "Municipal Offices, Garden Place, Hamilton, New Zealand"
            }]

        if available_slots:
            filtered_slots[inspector_id] = available_slots

    print("Available slots for inspectors:")
    print(filtered_slots)
    return filtered_slots

def get_distances(inspector_availability, inspection_location):
    """
    Calculates the distance and travel times from the last known location to the inspection location
    """
    inspector_distance_info_list = []
    for inspector_id, slots in inspector_availability.items():
        for slot in slots:
            #get last known location
            last_location = slot['last_known_location']
            print(f"fetching coords between {last_location} and {inspection_location}")
            #fetch distance between last location and inspection location
            distance_data = api_utils.fetch_open_distance_data(last_location, inspection_location)
            print(f"calculating distance between {last_location} and {inspection_location}")

            if distance_data:
                inspector_distance_info = {
                    "inspector_id": inspector_id,
                    "distance": distance_data['distance'],
                    "duration": distance_data['duration'],
                    "last_known_location": last_location,
                    "inspection_location": inspection_location
                }
                inspector_distance_info_list.append(inspector_distance_info)

    print("Inspector distances and durations:")
    print(inspector_distance_info_list)
    return inspector_distance_info_list


def get_suggestions(inspector_distance_info_list, inspector_availability):
    """
    Generate the top 3 time slot suggestions for inspections based on these factors:
    1. Sort by shortest travel time
    2. Prioritizing longest availbility gaps for each inspector (ensuring some spread of work across inspectors)
    3. Time variability in suggestions
    """
    #sort inspectors by shortest duration
    sorted_distances = sorted(inspector_distance_info_list, key=lambda x: x['duration'])

    suggestions = []

    for inspector_info in inspector_distance_info_list:
        inspector_id = inspector_info['inspector_id']
        travel_duration = inspector_info['duration']
        distance = inspector_info['distance']

        # Sort each inspector's available slots by longest duration, ensuring inspectors with larger time gaps in their schedules are considered first
        available_slots = sorted(inspector_availability[inspector_id], 
                                 key=lambda slot: slot['end'] - slot['start'], 
                                 reverse=True)  

        for slot in available_slots:
            #calculate adjusted start time by adding the travel duration
            adjusted_start_time = datetime.combine(datetime.today(), slot['start']) + timedelta(minutes=travel_duration)
            end_time = datetime.combine(datetime.today(), slot['end'])

            #ensure the adjusted slot accounts for the minimum 2 hour inspection time
            if end_time - adjusted_start_time >= timedelta(hours=2):
                adjusted_slot = {
                    "inspector_id": inspector_id,
                    "distance": inspector_info['distance'],
                    "duration": travel_duration,
                    "adjusted_time_slot": (adjusted_start_time.time(), end_time.time())
                }

                #if add to suggestions if there's at least a 30 min difference from other suggestions
                if all(abs((adjusted_start_time - datetime.combine(datetime.today(), s['adjusted_time_slot'][0])).total_seconds()) >= 1800 for s in suggestions):
                    suggestions.append(adjusted_slot)

    return suggestions



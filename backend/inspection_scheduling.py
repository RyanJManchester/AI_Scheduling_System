import api_utils
import psycopg2

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

    qualified_inspector_ids = []
    # Connect to the database and fetch all inspectors
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # SQL query to fetch all inspectors
    cursor.execute("SELECT id FROM Inspector")
    inspectors = cursor.fetchall()

    #iterate through inspectors in inspectors_data
    for inspector_data in inspectors:
        inspector_id = inspector_data[0]
        inspector = api_utils.Inspector.fetch_from_db(inspector_data['id'], db_params)
        # Determine which qualification list to check based on inspection type
        if inspection_type.startswith('R'):
            # Check residential qualifications
            qualifications_to_check = inspector.residential_quals
        else:
            # Check commercial qualifications
            qualifications_to_check = inspector.commercial_quals

        # Check if the inspector has any valid qualifications for the requested inspection type
        if any(qual in valid_qualifications for qual in qualifications_to_check):
            qualified_inspector_ids.append(inspector.id)

    print("Qualified inspectors:")
    print(qualified_inspector_ids)
    return qualified_inspector_ids

def get_available_schedules(working_hours, inspector_ids, inspection_date, db_params):
    """
    Gets the available time slots for inspectors based on their schedules from the database. 
    It only returns timeslots that longer than 2 hours.
    """
    filtered_slots = []

    for inspector_id in inspector_ids:
        #fetch inspector's schedule for the given date
        schedule = api_utils.Inspector.get_schedule_for_date(inspector_id, inspection_date, db_params)
import api_utils

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

def get_qualified_inspectors(inspectors_data, inspection_type):
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
    #iterate through inspectors in inspectors_data
    for inspector_data in inspectors_data:
        inspector = api_utils.Inspector.fetch_from_db(inspector_data['id'], inspector_data['db_params'])
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

def get_available_schedules(working_hours, schedules, inspection_date):
    """
    This function gets the available time slots based on inspector schedules.
    It is broken up into 2 prompts to the model to maintain accuracy
    Prompt 1: Filter inspections by date
    Prompt 2: Calculate available time slots
    Step 3: manually filter out timeslots that are shorter than 2 hours (this is done manually as the AI tends to hallucinate with this prompt)

    Args:
    - working_hours (str): The working hours of the inspectors.
    - schedules (dict): The JSON file with inspector schedules.
    - inspection_date (str): The date of the inspection.

    Returns:
    - str: The JSON string containing the available time slots for each inspector on the given date.
    """
    # Step 1: Filter inspections by date
    prompt_date_filter = f"""
    You are given the following schedules for each inspector:
    {json.dumps(schedules)}
    Your task is to remove the inspections not scheduled for the date {inspection_date}.
    1. For each inspector, remove all inspections from the json that do not occur on {inspection_date}.
    2. If an inspector has no inspections scheduled on {inspection_date}, return: "Available from {working_hours}".

    Ensure your response returns only the original input format with the inspections that occur on {inspection_date}.
    """
    available_slots_by_date = getResponse(prompt_date_filter).strip('```').replace('json\n', '').strip()
    print("Available slots by date: " + available_slots_by_date)

    #Step 2: calculate available slots
    prompt_initial_schedules = f"""
    You are given the following schedules for each inspector:
    {available_slots_by_date}

    Your task is to calculate the available time slots for each inspector on {inspection_date}.

    1. If there are inspections scheduled, calculate the remaining free time slots outside of these scheduled inspections.
    2. Ensure that the available time slots do not overlap with any scheduled inspections.
    3. For each inspector, consider the working hours as the total available time range (e.g., 09:00 to 17:00) and calculate the available slots accordingly.
    4. If an inspection ends at time A and another starts at time B, the time slot from A to B should be considered available if A < B.
    5. If multiple available time slots are adjacent to each other (e.g., one slot ends and another starts without a gap), combine them into a single time slot.
    6. Include the previous inspection location as the location of the last inspection prior to the available time slot.
     Use the following JSON example as a reference for the output:
        [
    {{
        "inspector_id": "inspector_id",
        "available_slots": [
        {{"start_time": "09:00", "end_time": "12:00", "previous_inspection_location": "123 Main St"}}
        ]
    }},
    {{
        "inspector_id": "inspector_id",
        "available_slots": [
        {{"start_time": "13:00", "end_time": "17:00", "previous_inspection_location": "456 Main St"}}
        ]
    }},
    {{
        "inspector_id": "inspector_id",
        "available_slots": "Available from 9am - 5pm", "previous_inspection_location": "N/A"
    }}
    ]
    The previous inspection location is the location of the inspection prior to the available time slot
     Ensure your response contains only valid available time slots and nothing else.
    """
    available_slots =getResponse(prompt_initial_schedules).strip('```').replace('json\n', '').strip()
    print("available slots: " + available_slots)

    #Step 3: Remove slots that are not at least 2 hours long
    filtered_slots = []
    slots_data = json.loads(available_slots) #load json file of inspector available slots

    #for every inspector, filter out slots that are not at least 2 hours long
    for inspector in slots_data:
        inspector_id = inspector['inspector_id']
        valid_slots = []

        if isinstance(inspector['available_slots'], str) and 'Available from' in inspector['available_slots']:
            # If the inspector is not available, keep this message.
            valid_slots.append(inspector['available_slots'])
        else:
            for slot in inspector['available_slots']:
                start_time_str = slot['start_time']
                end_time_str = slot['end_time']

                start_time = datetime.strptime(start_time_str, '%H:%M')
                end_time = datetime.strptime(end_time_str, '%H:%M')

                # Calculate duration in minutes
                duration_minutes = (end_time.hour * 60 + end_time.minute) - (start_time.hour * 60 + start_time.minute)

                if duration_minutes >= 120:  # Check if the duration is at least 120 minutes (2 hours)
                    valid_slots.append(slot)

        if valid_slots:
            filtered_slots.append({
                'inspector_id': inspector_id,
                'available_slots': valid_slots
            })

    print("Filtered slots: " + json.dumps(filtered_slots, indent=2))
    return json.dumps(filtered_slots)

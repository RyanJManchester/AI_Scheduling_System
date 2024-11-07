import psycopg2
from psycopg2 import sql

class BuildingConsent:    
    def __init__(self, bc_number, level=None, location=None, db_params=None):
        """
        Initialize a BuildingConsent instance, either with new data or from an existing record in the database.
        """
        self._bc_number = bc_number
        self._level = level
        self._location = location
        self.db_params = db_params

    def save(self):
        """
        Add this BuildingConsent to the database if it does not exist; or updates it if it does exist
        """
        if self._bc_number is None:
            raise ValueError("Building Consent number must be set for saving.")

        with psycopg2.connect(**self.db_params) as conn:
            with conn.cursor() as cursor:
                # Check if bc_number already exists
                cursor.execute("SELECT * FROM Building_Consent WHERE bc_number = %s", (self._bc_number,))
                exists = cursor.fetchone()

                if exists:
                    # Update existing record
                    cursor.execute("""
                        UPDATE Building_Consent SET level = %s, location = %s WHERE bc_number = %s
                    """, (self._level, self._location, self._bc_number))
                else:
                    # Insert new record
                    cursor.execute("""
                        INSERT INTO Building_Consent (bc_number, level, location)
                        VALUES (%s, %s, %s)
                    """, (self._bc_number, self._level, self._location))
                conn.commit()

    @classmethod
    def fetch_from_db(cls, bc_number, db_params):
        """
        Fetches a building consent by its bc_number and returns an instance of BuildingConsent
        """
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        cursor.execute("SELECT bc_number, level, location FROM Building_Consent WHERE bc_number = %s", (bc_number,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return cls(bc_number=result[0], level=result[1], location=result[2], db_params=db_params)
        else:
            raise ValueError(f"Building Consent with bc_number {bc_number} not found.")


    def delete(self):
        """
        Delete this BuildingConsent from the database.
        """
        if self.bc_number is None:
            raise ValueError("Cannot delete Building Consent without a bc_number.")
        
        conn = psycopg2.connect(**self.db_params)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Building_Consent WHERE bc_number = %s", (self.bc_number,))

        conn.commit()
        cursor.close()
        conn.close()

    def update(self, level=None, location=None):
        """
        Update this BuildingConsent in the database.
        """
        if level is not None:
            self.level = level
        if location is not None:
            self.location = location

        self.save()

    def get_inspections(self):
        """
        Gets all inspections related to this Building Consent from the view
        """
        with psycopg2.connect(**self.db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT inspection_id, bc_number, description, date, time, inspector_id,status, building_address, owner_name, order
                    FROM BuildingConsentInspectionsView
                    WHERE bc_number = %s
                    ORDER BY order;
                """, (self._bc_number,))
                inspections = cursor.fetchall()

        #convert result to a list of dictionaries
        inspections_list = []
        for inspection in inspections:
            inspections_list.append({
                'inspection_id': inspection[0],
                'bc_number': inspection[1],
                'description': inspection[2],
                'date': inspection[3],
                'time': inspection[4],
                'inspector_id': inspection[5],
                'status': inspection[6],
                'building_address': inspection[7],
                'owner_name': inspection[8],
                'order': inspection[9]
            })
            return inspections_list

    @property
    def bc_number(self):
        """
        Get the building consent number
        """        
        return self._bc_number

    @property
    def level(self):
        """
        Get the building consent level
        """
        return self._level

    @property
    def location(self):
        """
        Get the building consent location
        """
        return self._location


# ## Example Usage

# # Adding a new building consent
# consent = BuildingConsent(bc_number=1, level="R1", location="1 Smith Street", db_params=db_params)
# consent.save() 

# # Fetching an existing building consent
# fetched_consent = BuildingConsent.fetch_from_db(bc_number=1, db_params=db_params)
# print(f"Fetched Consent: {fetched_consent.level}, {fetched_consent.location}")

# # Updating the level and location
# fetched_consent.update(level="R2", location="2 Smith Street")
# print(f"Updated Consent: {fetched_consent.level}, {fetched_consent.location}")

# # Deleting the building consent
# fetched_consent.delete()
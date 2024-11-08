import psycopg2
from psycopg2 import sql

class Inspector: 
    def __init__(self, id=None, name=None, email=None, residential_qual=None, commercial_qual=None, db_params=None):
        """
        Initialize an Inspector instance, either with new data or from an existing record in the database.
        """
        self._id = id
        self._name = name
        self._email = email
        self._residential_qual = residential_qual
        self._commercial_qual = commercial_qual 
        self.db_params = db_params

    
    def save(self):
        """
        Add this Inspector to the database if it does not exist; or updates it if it does exist.
        """
        conn = psycopg2.connect(**self.db_params)
        cursor = conn.cursor()

        if self.id is None and self.email is None and self.residential_qual is None and self.commercial_qual is None:
            raise ValueError("Inspector ID, email, and inspector qualifications must be set for saving.")
        
        # Check if the inspector already exists based on the email
        cursor.execute("SELECT * FROM Inspector WHERE email = %s", (self.email,))
        exists = cursor.fetchone()

        if exists:
            # Update existing record
            cursor.execute("""
                           UPDATE Inspector SET name = %s, email = %s, residential_quals = %s, commercial_quals = %s WHERE id = %s""", (self.name, self.email, ','.join(self.residential_quals), ','.join(self.commercial_quals),self.id))
        else:
            # Insert new record
            cursor.execute("""
                INSERT INTO Inspector (name, email, residential_quals, commercial_quals) 
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (self.name, self.email, ','.join(self.residential_quals), ','.join(self.commercial_quals)))
            self.id = cursor.fetchone()[0]  # Set the ID from the newly created record
        
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def fetch_from_db(cls, inspector_id, db_params):
        """
        Fetches an inspector by its ID and returns an instance of Inspector.
        """
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, email, residential_qual, commercial_qual FROM Inspector WHERE id = %s", (inspector_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return cls(id=result[0], name=result[1], email=result[2], residential_qual=result[3], commercial_qual=result[4], db_params=db_params)
        else:
            raise ValueError(f"Inspector with ID {inspector_id} not found.")
        
    @classmethod
    def get_schedule_for_date(cls, inspector_id, date, db_params):
        """
        gets the schedule for an inspector on a specific date
        """
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        query="""
                SELECT * FROM InspectorScheduleView where inspector_id = %s and inspection_date = %s
            """
        cursor.execute(query, (inspector_id, date))
        schedule = cursor.fetchall()

        #convert schedule to list of dict for handling
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in schedule]

        cursor.close()
        conn.close()

        return result

    def delete(self):
        """
        Delete this Inspector from the database.
        """
        if self.id is None:
            raise ValueError("Cannot delete Inspector without an ID.")
        
        conn = psycopg2.connect(**self.db_params)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Inspector WHERE id = %s", (self.id,))

        conn.commit()
        cursor.close()
        conn.close()
    
    def update(self, name=None, email=None, residential_quals=None, commercial_quals=None):
        """
        Update this Inspector in the database.
        """
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if residential_quals is not None:
            self.residential_quals = residential_quals
        if commercial_quals is not None:
            self.commercial_quals = commercial_quals

        self.save()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email
    
    @property
    def residential_qual(self):
        return self._residential_qual

    @property
    def commercial_qual(self):
        return self._commercial_qual
    
        
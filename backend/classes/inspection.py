import psycopg2
from psycopg2 import sql

class Inspection:
    def __init__(self, id=None, bc_number=None, description=None, date=None, start_time=None, end_time=None, inspector_id=None, status="Scheduled", order=None, db_params=None):
        """
        Initialize an Inspection instance, either with new data or from an existing record in the database.
        """
        self._id = id
        self._bc_number = bc_number
        self._description = description
        self._date = date
        self._start_time = start_time
        self._end_time = end_time
        self._inspector_id = inspector_id
        self._status = status
        self._order = order
        self.db_params = db_params

    def save(self):
        """
        Add this Inspection to the database if it does not exist; or updates it if it does exist.
        """
        conn = psycopg2.connect(**self.db_params)
        cursor = conn.cursor()

        if self.id is None:
            raise ValueError("Inspection id must be set for saving.")

        # check if id already exists
        cursor.execute("SELECT * FROM inspection WHERE id = %s", (self.id,))
        exists = cursor.fetchone()

        if exists:
            # update existing record with id
            cursor.execute("""
                UPDATE Inspection SET bc_number = %s, description = %s, date = %s, start_time = %s, end_time=%s, inspector_id = %s, status = %s, order = %s WHERE id = %s
                """,(self.bc_number, self.description, self.date, self.start_time, self.end_time, self.inspector_id, self.status, self.order, self.id))
        else:
            # insert new record
            cursor.execute("""
                INSERT INTO Inspection (bc_number, description, date, time, inspector_id, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                """, (self.bc_number, self.description, self.date, self.start_time, self.end_time, self.inspector_id, self.status, self.order))
            self.id = cursor.fetchone()[0] #set ID from newly created record

        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def fetch_from_db(cls, id, db_params):
        """
        Fetches an inspection by its id and returns an instance of Inspection
        """
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        cursor.execute("SELECT id, bc_number, description, date, time, inspector_id, statu, order FROM Inspection WHERE id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return cls(
                id=result[0],
                bc_number=result[1],
                description=result[2],
                date=result[3],
                start_time=result[4],
                end_time=result[5],
                inspector_id=result[6],
                status=result[7],
                order=result[8],  
                db_params=db_params
            )
        else:
            raise ValueError(f"Inspection with ID: {id} not found.")
        
    def delete(self):
        """
        Delete this Inspection from the database.
        """
        if self.id is None:
            raise ValueError("Cannot delete Inspection without an id.")
        
        conn = psycopg2.connect(**self.db_params)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Inspection WHERE id = %s", (self.id,))

        conn.commit()
        cursor.close()
        conn.close()

    def update(self, bc_number=None, description=None, date=None, start_time=None,  end_time=None, inspector_id=None, status=None, order=None):
        """
        Update this Inspection's attributes.
        """
        if bc_number is not None:
            self.bc_number = bc_number
        if description is not None:
            self.description = description
        if date is not None:
            self.date = date
        if start_time is not None:
            self.start_time = start_time
        if end_time is not None:
            self.end_time = end_time
        if inspector_id is not None:
            self.inspector_id = inspector_id
        if status is not None:
            self.status = status
        if order is not None:
            self.order = order

        self.save()

    @property
    def id(self):
        return self._id

    @property
    def bc_number(self):
        return self._bc_number

    @property
    def description(self):
        return self._description

    @property
    def date(self):
        return self._date

    @property
    def start_time(self):
        return self._start_time
    
    @property
    def end_time(self):
        return self._end_time

    @property
    def inspector_id(self):
        return self._inspector_id

    @property
    def status(self):
        return self._status

    @property
    def order(self):
        return self._order  
    

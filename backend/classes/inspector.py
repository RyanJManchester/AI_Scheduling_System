import pyscopg2
from psycopg2 import sql

class Inspector: 
    def __init__(self, id=None, name=None, email=None, db_params=None):
        """
        Initialize an Inspector instance, either with new data or from an existing record in the database.
        """
        self.id = id
        self.name = name
        self.email = email
        self.db_params = db_params
    
    def save(self):
        """
        Add this Inspector to the database if it does not exist; or updates it if it does exist.
        """
        conn = psycopg2.connect(**self.db_params)
        cursor = conn.cursor()

        if self.id is None and self.email is None:
            raise ValueError("Inspector ID or email must be set for saving.")
        
        # Check if the inspector already exists based on the email
        cursor.execute("SELECT * FROM Inspector WHERE email = %s", (self.email,))
        exists = cursor.fetchone()

        if exists:
            # Update existing record
            cursor.execute("""
                UPDATE Inspector SET name = %s, email = %s WHERE id = %s
                           """, (self.name, self.email, self.id))
        else:
            # Insert new record
            cursor.execute("""
                INSERT INTO Inspector (name, email) VALUES (%s, %s) RETURNING id
            """, (self.name, self.email))
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

        cursor.execute("SELECT id, name, email FROM Inspector WHERE id = %s", (inspector_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return cls(id=result[0], name=result[1], email=result[2], db_params=db_params)
        else:
            raise ValueError(f"Inspector with ID {inspector_id} not found.")
        
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
    
    def update(self, name=None, email=None):
        """
        Update this Inspector in the database.
        """
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email

        self.save()

    @property
    def get_id(self):
        return self.id

    @property
    def get_name(self):
        return self.name

    @property
    def get_email(self):
        return self.email
    
        